class Page
    @pages = {}
    @current_page = null
    @first = true

    @load: (page, scrollto, updatenav) ->
        if !page
            page = @current_page

        if updatenav
            @push_nav(page, scrollto)

        if @current_page != page
            # Load <page>.xml from the xml/ dir
            if !(page in @pages)

                $.ajax({
                    url: 'xml/' + page + '.xml',
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

        @scroll(page, scrollto)

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

        if !id
            return '#' + page.replace('#', '/')
        else
            return '#' + page + '/' + id

    @load_ref: (ref) ->
        r = ref.split('#')
        @load(r[0], r[1], true)

    @load_description: (page, content) ->
        doc = new Doc(page.children('doc')).render()

        if doc
            content.append($('<h1>Description</h1>'))
            desc = $('<div class="description"/>')

            desc.append(doc)
            content.append(desc)

    @load_items: (page, content) ->
        all = page.children()

        for group in Node.groups
            items = all.filter(group)

            if items.length == 0
                continue

            typename = items.tag()[0]

            if !(typename of Node.types)
                continue

            type = Node.types[typename]

            h1 = $('<h1/>').text(type.title)
            h1.appendTo(content)

            container = type.render_container()

            for item in items
                new type($(item)).render(container)

            if container
                content.append(container)

    @load_contents: (page) ->
        content = $('#content')
        content.empty()

        @load_description(page, content)
        @load_items(page, content, 'Type definitions', 'typedef:not([access])')

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

    @select: (scrollto) ->
        if @selected_element
            @selected_element.removeClass('selected')
            @selected_element = null

        e = document.getElementById(scrollto)

        if e
            @selected_element = $(e)
            @selected_element.addClass('selected')

    @scroll: (page, scrollto) ->
        if !scrollto
            return

        if page == null
            page = @current_page

        @select(scrollto)
        e = document.getElementById(scrollto)

        if e
            top = $(e).offset().top - 10

            if @first
                $('html, body').scrollTop(top)
            else
                $('html, body').animate({scrollTop: top}, 1000, 'easeInOutExpo')
        else
            @selected_element = null

        @first = false

# vi:ts=4:et
