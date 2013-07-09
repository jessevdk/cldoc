cldoc.SearchWorker = ->
    db = null

    log = (msg) ->
        self.postMessage({type: 'log', message: msg})

    load_db = (host) ->
        xhr = new XMLHttpRequest()
        xhr.open('GET', host + '/search.json?' + new Date().getTime(), false)
        xhr.send()

        return JSON.parse(xhr.responseText)

    bsearch = (term, l, r, sel) =>
        suffix_record = (i) => db.suffixes[i][0]

        while l < r
            mid = Math.floor((l + r) / 2)

            rec = suffix_record(mid)
            suf = db.records[rec[0]][0].substring(rec[1])

            [l, r] = if sel(suf) then [mid + 1, r] else [l, mid]

        return [l, r]

    search_term = (term) =>
        if term.length < 3
            return [0, 0]

        l = 0
        r = db.suffixes.length

        t = term.toLowerCase()

        [start, _] = bsearch(t, 0, db.suffixes.length,
                             (suf) -> t > suf
        )

        [_, end] = bsearch(t, start, db.suffixes.length,
                           (suf) -> suf.indexOf(t) == 0
        )

        return [start, end]

    self.onmessage = (ev) =>
        m = ev.data

        if db == null
            db = load_db(m.host)

        words = m.q.split(/\s+/)

        records = {}

        ret = {type: 'result', id: m.id, q: m.q, words: words, records: []}

        for word in words
            [start, end] = search_term(word)

            for i in [start..(end - 1)] by 1
                items = db.suffixes[i]

                for rec in items
                    recid = rec[0]

                    if !(recid of records)
                        rr = {
                            name: db.records[recid][0],
                            id: db.records[recid][1],
                            score: 0,
                            results: [],
                            suffixhash: {},
                        }

                        ret.records.push(rr)
                        records[recid] = rr
                    else
                        rr = records[recid]

                    if !(rec[1] of rr.suffixhash)
                        rr.score += 1
                        rr.results.push([rec[1], rec[1] + word.length])

                        rr.suffixhash[rec[1]] = true

        ret.records.sort((a, b) -> a.score > b.score ? (a.score < b.score ? -1 : 0))
        self.postMessage(ret)

class cldoc.SearchDb
    constructor: ->
        @searchid = 0
        @searchcb = null

        wurl = window.webkitURL ? window.URL

        blob = new Blob(['worker = ' + cldoc.SearchWorker.toString() + '; worker();'],
                        {type: 'text/javascript'})

        @worker = new Worker(wurl.createObjectURL(blob))

        @worker.onmessage = (msg) =>
            m = msg.data

            if m.type == 'log'
                console.log(m.message)
            else if m.type == 'result'
                if m.id != @searchid
                    return

                @searchid = 0
                @searchcb(m)

    search: (q, cb) ->
        # Split q in "words"
        @searchid += 1
        @searchcb = cb

        @worker.postMessage({type: 'search', q: q, id: @searchid, host: cldoc.host})

class cldoc.Page
    @pages = {}
    @current_page = null
    @first = true

    @search = {
        db: null,
    }

    @request_page: (page, cb) ->
        if page of @pages
            cb(@pages[page])
            return

        url = cldoc.host + '/xml/' + page + '.xml'

        $.ajax({
            url: url,
            cache: false,
            success: (data) =>
                @pages[page] = {xml: $(data), html: null}
                cb(@pages[page])
        })

    @load: (page, scrollto, updatenav) ->
        cldoc.Sidebar.exit_search()

        if page == null || page == 'undefined'
            page = @current_page

        if !page
            page = 'index'

        if updatenav
            @push_nav(page, scrollto)

        if @current_page != page
            # Load <page>.xml from the xml/ dir if needed
            @request_page(page, => @load_page(page, scrollto))
        else
            @scroll(page, scrollto)

    @make_link: (ref, name, attrs = {}) ->
        e = cldoc.html_escape

        r = @make_internal_ref(ref)
        ret = '<a href="' + e(r) + '"'

        for k, v of attrs
            ret += ' ' + k + '="' + e(v) + '"'

        return ret + '>' + e(name) + '</a>'

    @load_page: (page, scrollto) ->
        @first = @current_page == null
        start = new Date();

        @current_page = page
        cpage = @pages[page]

        data = cpage.xml
        html = cpage.html

        $('#cldoc #cldoc_content').children().detach()

        root = data.children(':first')

        if html
            $('#cldoc #cldoc_content').append(html.content)
            cldoc.Sidebar.load_html(html.sidebar)
        else
            sidebar = cldoc.Sidebar.load(root)
            content = @load_contents(root)

            cpage.html = {
                sidebar: sidebar,
                content: content
            }

        title = root.attr('name')

        if !title
            brief = root.children('brief')

            if brief.length > 0
                title = brief.text()

                if title[title.length - 1] == '.'
                    title = title.substring(0, title.length - 1)

        if !title
            title = 'Documentation'

        document.title = title

        @scroll(page, scrollto, true)
        $('#cldoc').triggerHandler('page-loaded', [root])

    @make_external_ref: (page, id) ->
        if page[0] == '#'
            page = page.substring(1)

        if !id
            return page.replace('/', '#')
        else
            return page + '#' + id

    @make_internal_ref: (page, id) ->
        # External refs (like those in the xml) use the <page>#<part> syntax.
        # However, on the page we use the #<page>/<part> syntax so we can
        # easily manipulate history and keep urls on one single entry point

        if !page
            return '#index'

        if !id
            return '#' + page.replace('#', '/')
        else
            return '#' + page + '/' + id

    @split_ref: (ref) ->
        [page, id] = ref.split('#', 2)

        if !page
            page = 'index'

        return [page, id]

    @load_ref: (ref) ->
        r = @split_ref(ref)
        @load(r[0], r[1], true)

    @make_header: (item) ->
        id = item.attr('id')
        e = cldoc.html_escape

        if id
            ret = '<span>'

            type = @node_type(item)
            title = item.attr('title')

            if type
                ret += '<span class="keyword">' + e(type.title[0]) + '</span>'
                obj = new type(item)

                name = obj.full_name_for_display
            else
                name = item.attr('name')

            if title
                ret += '<span>' + e(title) + '</span>'
            else
                if name
                    ret += '<span>' + e(name) + '</span>'
                else
                    ret += '<span>' + e(id) + '</span>'

            return ret
        else
            return ''

    @load_description: (page, content) ->
        doc = cldoc.Doc.either(page)

        id = page.attr('id')

        if id
            h1 = $('<h1/>').appendTo(content)
            h1.attr('id', id)

            h1.append(@make_header(page))

        if doc
            desc = $('<div class="description"/>')

            desc.append(doc)
            content.append(desc)

    @node_type: (item) ->
        typename = cldoc.tag(item)[0]

        if !(typename of cldoc.Node.types)
            return null

        return cldoc.Node.types[typename]

    @load_items: (page) ->
        all = page.children()
        content = ''
        e = cldoc.html_escape

        for group in cldoc.Node.groups
            items = all.filter(group)

            if items.length == 0
                continue

            type = @node_type(items)

            if !type || type == cldoc.Node.types.report
                continue

            content += '<h2 data-cldoc-dynamic="1" id="' + e(type.title[1].toLowerCase()) + '">' + e(type.title[1]) + '</h2>'

            container = type.render_container()
            itemcontents = ''

            for item in items
                item = $(item)

                if cldoc.tag(item)[0] != cldoc.tag(items)[0]
                    tp = @node_type(item)
                else
                    tp = type

                if tp
                    ret = new tp($(item)).render()

                    if ret
                        itemcontents += ret

            if container
                content += container[0] + itemcontents + container[1]
            else
                content += itemcontents

        return content

    @bind_links: (container) ->
        container.find('a').on('click', (e) =>
            ref = $(e.delegateTarget).attr('href')

            if ref[0] == '#'
                @load_ref(@make_external_ref(ref))
                return false
            else
                return true
        )

    @load_pagenav: (page, content) ->
        if @node_type(page) != cldoc.Category
            return

        pagenav = $('#cldoc_sidebar_pagenav')
        ul = $('<ol/>')

        h2cnt = 0
        h2li = null
        h2ol = null
        h3cnt = 0

        content.find('h2,h3').each((i, e) =>
            h = $(e)

            if h.attr('data-cldoc-dynamic')
                return

            id = h.text()

            ish2 = e.tagName == 'H2'

            if ish2
                h2cnt += 1
                t = h2cnt + '. ' + id
            else
                h3cnt += 1
                t = h2cnt + '.' + h3cnt + '. ' + id

            h.text(t)
            h.attr('id', id)

            a = $('<a/>', href: @make_internal_ref(@current_page, id)).text(t)

            li = $('<li/>').append(a)

            if !ish2 && h2li != null
                if h2ol == null
                    h2ol = $('<ol/>').appendTo(h2li)

                h2ol.append(li)
            else
                if ish2 && h2li == null
                    h2li = li
                    h2ol = null

                li.appendTo(ul)
        )

        @bind_links(ul)

        pagenav.append(ul)

    @load_contents: (page) ->
        content = $('#cldoc #cldoc_content')
        content.children().detach()

        @load_description(page, content)

        items = $(@load_items(page))
        content.append(items)
        @bind_links(content)

        @load_pagenav(page, content)

        return content.children()

    @push_nav: (page, scrollto) ->
        hash = document.location.hash
        [prevpage, prevscrollto] = @split_ref(@make_external_ref(hash))

        history.pushState({page: prevpage, scrollto: prevscrollto}, page, @make_internal_ref(page, scrollto))

    @route: ->
        # Routing
        hash = document.location.hash.substr(1)
        route = new RegExp('^([^/]+)(/(.*))?$')

        m = route.exec(hash)

        page = ''
        scrollto = ''

        if !m
            page = 'index'
        else
            page = m[1]
            scrollto = m[3]

        $(window).on('popstate', (e) =>
            if e.originalEvent.state
                state = e.originalEvent.state

                # Only reload if the page is not the same as the current page.
                # Browsers already scroll automatically to the previous state
                if state.page != @current_page
                    @load(state.page, state.scrollto, false)
                else
                    @select(state.scrollto, false)
        )

        @load(page, scrollto)

    @select: (scrollto, doanimate) ->
        scrollto = $(scrollto)

        if !scrollto && !@selected_element
            return

        if scrollto && @selected_element && scrollto.attr('id') == @selected_element.attr('id')
            return

        if doanimate
            inopts = {'duration': 2000, 'easing': 'easeInOutExpo'}
            outopts = {'duration': 100, 'easing': 'easeInOutExpo'}
        else
            inopts = {'duration': 0}
            outopts = {'duration': 0}

        if @selected_element
            @selected_element.removeClass('selected', outopts)
            @selected_element = null

        if scrollto
            @selected_element = $(scrollto)
            @selected_element.addClass('selected', inopts)

    @scroll: (page, scrollto, newpage) ->
        if !scrollto
            return

        if page == null
            page = @current_page

        e = $(document).find('#' + scrollto.replace(/([:() ])/g, '\\$1')).first()

        if e && e.length > 0
            e = $(e)
            top = e.offset().top - 10

            istopandnew = (newpage && e.is('h1'))

            if @first || istopandnew
                if !istopandnew
                    @select(e)
                else
                    @select()

                $('html, body').scrollTop(top)
            else
                @select(e, true)
                $('html, body').animate({scrollTop: top}, 1000, 'easeInOutExpo')
        else
            @select(null, true)

        @first = false

    @render_search: (result) ->
        # Detach the current page
        content = $('#cldoc_content')

        content.children().detach()

        $('<h1><span class="keyword">Search</span> </h1>').append(result.q).appendTo(content)

        if result.records.length == 0
            $('<span class="info">There were no results for this search query.</span>').appendTo(content)
            cldoc.Sidebar.render_search([])

            $('html, body').scrollTop(0)
            return

        records = []

        # Resolve records to add brief docs and type info
        for res in result.records
            # Multiple results with the same suffix...
            [page, pageid] = @split_ref(res.id)

            if not page of @pages
                continue

            cpage = @pages[page]
            data = cpage.xml

            pageidesc = pageid.replace(/([:() ])/g, '\\$1')
            item = data.find('#' + pageidesc)

            if item.length != 1
                continue

            tag = cldoc.tag(item)[0]

            res.type = tag
            res.brief = new cldoc.Doc(item.children('brief'))
            res.page = page
            res.qid = pageid

            records.push(res)

        # Sort results based on score, type and finally name
        sortfunc = (a, b) ->
            if a.score != b.score
                return if a.score > b.score then -1 else 1

            if a.type != b.type
                ai = cldoc.Node.order[a.type]
                bi = cldoc.Node.order[b.type]

                if ai != bi
                    return if ai < bi then -1 else 1

            return if a.name < b.name then -1 else 1

        records.sort(sortfunc)

        t = $('<table class="search_results"/>').appendTo(content)

        for res in records
            # Highlight matches
            res.results.sort((a, b) ->
                if a[0] != b[0]
                    return if a[0] < b[0] then -1 else 1

                if a[1] > b[1]
                    return -1

                if a[1] < b[1]
                    return 1

                return 0)

            prev = 0
            parts = []

            for [start, end] in res.results
                if start < prev
                    continue

                parts.push(res.qid.substring(prev, start))
                parts.push($('<span class="search_result"/>').text(res.qid.substring(start, end)))
                prev = end

            parts.push(res.qid.substring(prev, res.qid.length))

            a = $('<a/>', {href: @make_internal_ref(res.id)}).html(parts)

            a.on('click', do (res) =>
                => @load_ref(res.id)
            )

            $('<tr/>').append($('<td class="keyword"/>').text(res.type))
                      .append($('<td class="identifier"/>').html(a))
                      .appendTo(t)

            $('<tr/>').append($('<td/>'))
                      .append($('<td/>').html(res.brief.render()))
                      .appendTo(t)

        cldoc.Sidebar.render_search(records)
        $('html, body').scrollTop(0)

    @search_result: (result) ->
        # First prefetch all the pages to access the docs and type info etc.
        pagereqcount = 0
        pages = {}

        for record in result.records
            [page, pageid] = @split_ref(record.id)

            if page of pages
                continue

            pagereqcount += 1
            pages[page] = true

        if pagereqcount == 0
            @render_search(result)

        for page of pages
            @request_page(page, =>
                pagereqcount -= 1

                if pagereqcount == 0
                    @render_search(result)
            )

    @search: (q) ->
        if q.length < 3
            return false

        # First make sure to load the search db
        if !@search.db
            @search.db = new cldoc.SearchDb()

        @search.db.search(q, (res) => @search_result(res))
        return true

    @exit_search: ->
        ref = Page.make_external_ref(document.location.hash.substring(1))
        cldoc.Sidebar.exit_search()

        @current_page = null
        @load_ref(ref)

# vi:ts=4:et
