cldoc.SearchWorker = ->
    db = null

    log = (msg) ->
        self.postMessage({type: 'log', message: msg})

    load_db = ->
        xhr = new XMLHttpRequest()
        xhr.open('GET', 'http://localhost:6060/search.json?' + new Date().getTime(), false)
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
        if db == null
            db = load_db()

        m = ev.data
        words = m.q.split(/\s+/)

        ret = {type: 'result', id: m.id, q: m.q, words: words, records: {}, results: []}

        for word in words
            [start, end] = search_term(word)

            for i in [start..(end - 1)] by 1
                items = db.suffixes[i]

                for rec in items
                    recid = rec[0]

                    if !(recid of ret.records)
                        ret.records[recid] = db.records[recid]

                ret.results[i - start] = items

            self.postMessage(ret)

class cldoc.SearchDb
    constructor: ->
        @searchid = 0

        wurl = window.webkitURL ? window

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
                console.log(m)

    search: (q) ->
        # Split q in "words"
        @searchid += 1
        @worker.postMessage({type: 'search', q: q, id: @searchid})

class cldoc.Page
    @pages = {}
    @current_page = null
    @first = true

    @search = {
        db: null,
        original_content: null
    }

    @request_page: (page, cb) ->
        if page in @pages
            cb(@pages[page])
            return

        if page == '(report)'
            url = 'report.xml'
        else
            url = 'xml/' + page + '.xml'

        $.ajax({
            url: url,
            cache: false,
            success: (data) =>
                @pages[page] = $(data)
                cb(@pages[page])
        })

    @load: (page, scrollto, updatenav) ->
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

    @know_more: (ref) ->
        a = @make_link(ref, 'more information on separate page...')
        a.addClass('know_more')

        return a

    @make_link: (ref, name) ->
        a = $('<a/>', {href: @make_internal_ref(ref)}).text(name)
        a.on('click', => @load_ref(ref); false)

        return a

    @load_page: (page, scrollto) ->
        @current_page = page
        data = @pages[page]

        $('#cldoc #cldoc_content').empty()

        root = data.children(':first')

        cldoc.Sidebar.load(root)
        @load_contents(root)

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
            return '/'

        if !id
            return '#' + page.replace('#', '/')
        else
            return '#' + page + '/' + id

    @load_ref: (ref) ->
        r = ref.split('#')
        @load(r[0], r[1], true)

    @make_header: (item) ->
        id = item.attr('id')

        if id
            ret = $('<span/>')

            type = @node_type(item)

            if type
                $('<span class="keyword"/>').text(type.title[0]).appendTo(ret)

            title = item.attr('title')

            if title
                $('<span/>').text(title).appendTo(ret)
            else
                $('<span/>').text(id).appendTo(ret)

            return ret
        else
            return null

    @load_description: (page, content) ->
        doc = new cldoc.Doc(page.children('doc')).render()

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

    @load_items: (page, content) ->
        all = page.children()

        for group in cldoc.Node.groups
            items = all.filter(group)

            if items.length == 0
                continue

            type = @node_type(items)

            if !type || type == cldoc.Node.types.report
                continue

            h2 = $('<h2/>').text(type.title[1])
            h2.attr('id', type.title[1].toLowerCase())
            h2.appendTo(content)

            container = type.render_container()

            for item in items
                item = $(item)

                if cldoc.tag(item)[0] != cldoc.tag(items)[0]
                    tp = @node_type(item)
                else
                    tp = type

                if tp
                    new tp($(item)).render(container)

            if container
                content.append(container)

    @load_contents: (page) ->
        content = $('#cldoc #cldoc_content')
        content.empty()

        @load_description(page, content)
        @load_items(page, content)

    @push_nav: (page, scrollto) ->
        history.pushState({page: page, scrollto: scrollto}, page, @make_internal_ref(page, scrollto))

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
                    @select(state.scrollto)
            else
                @load(page, scrollto)
        )

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

        e = document.getElementById(scrollto)

        if e
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

    @search_result: (result) ->
        true

    @search: (q) ->
        if q.length < 3
            return false

        # First make sure to load the search db
        if !@search.db
            @search.db = new cldoc.SearchDb()

        @search_result(@search.db.search(q))
        return true

    @exit_search: ->
        false

# vi:ts=4:et
