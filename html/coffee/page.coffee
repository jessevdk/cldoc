class Page
    @pages = {}
    @current_page = null
    @first = true

    @load: (page, scrollto, updatenav) ->
        if page == null || page == 'undefined'
            page = @current_page

        if !page
            page = 'index'

        if updatenav
            @push_nav(page, scrollto)

        if @current_page != page
            # Load <page>.xml from the xml/ dir
            if !(page in @pages)
                if page == '(report)'
                    url = 'report.xml'
                else
                    url = 'xml/' + page + '.xml'

                $.ajax({
                    url: url,
                    cache: false,
                    success: (data) =>
                        @pages[page] = $(data)
                        @load_page(page, scrollto)
                })

            else
                @load_page(page, scrollto)
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

        $('#content').empty()

        root = data.children(':first')

        Sidebar.load(root)
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
        doc = new Doc(page.children('doc')).render()

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
        typename = item.tag()[0]

        if !(typename of Node.types)
            return null

        return Node.types[typename]

    @load_items: (page, content) ->
        all = page.children()

        for group in Node.groups
            items = all.filter(group)

            if items.length == 0
                continue

            type = @node_type(items)

            if !type || type == Node.types.report
                continue

            h2 = $('<h2/>').text(type.title[1])
            h2.attr('id', type.title[1].toLowerCase())
            h2.appendTo(content)

            container = type.render_container()

            for item in items
                item = $(item)

                if item.tag()[0] != items.tag()[0]
                    tp = @node_type(item)
                else
                    tp = type

                if tp
                    new tp($(item)).render(container)

            if container
                content.append(container)

    @load_contents: (page) ->
        content = $('#content')
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

# vi:ts=4:et
