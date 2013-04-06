class cldoc.Sidebar
    @init: ->
        sidebar = $('#cldoc #cldoc_sidebar')

        if !sidebar
            return

        items = $('<div/>').attr('id', 'cldoc_sidebar_items')
        it = items[0]

        items.on('DOMSubtreeModified', (e) =>
            if it.scrollHeight > it.clientHeight
                $(it).removeClass('hide_scrollbar')
            else
                $(it).addClass('hide_scrollbar')
        )

        sidebar.append(items)

        div = $('<div/>').attr('id', 'cldoc_search')
        icon = $('<div class="icon"/>')
        close = $('<div class="close" title="Cancel search"/>')

        input = $('<input type="text" accesskey="s" title="Search documentation (Alt+S)"/>')

        items = $().add(div).add(icon).add(close)

        input.on('focus', (e) ->
            items.addClass('focus')
        )

        $('body').on('keydown', (e) ->
            if e.altKey && e.keyCode == 83
                input.focus()
                input.select()

                return true
        )

        input.on('blur', -> items.removeClass('focus'))
        icon.on('click', -> input.focus())

        exitsearch = ->
            input.val('')
            input.blur()
            cldoc.Page.exit_search()

        close.on('click', exitsearch)

        input.on('keypress', (e) ->
            if e.which == 13
                cldoc.Page.search(input.val())
                return true
        )

        input.on('keydown', (e) ->
            if e.keyCode == 27
                exitsearch()
        )

        div.append(icon)
        div.append(input)
        div.append(close)

        sidebar.append(div)

    @render_search: (results) ->
        $('#cldoc_sidebar').addClass('search')

    @exit_search: ->
        $('#cldoc_sidebar').removeClass('search')

    @load_html: (html) ->
        items = $('#cldoc #cldoc_sidebar #cldoc_sidebar_items')
        items.children().detach()

        items.append(html)

    @load: (page) ->
        items = $('#cldoc #cldoc_sidebar #cldoc_sidebar_items')

        if items.length == 0
            return null

        items.children().detach()

        head = cldoc.Page.make_header(page)

        if head
            div = $('<div class="back"/>')
            name = $('<div class="name"/>')

            name.append(head)
            div.append(name)
            items.append(div)

            id = page.attr('id')
            parts = id.split('::')

            l = parts.slice(0, parts.length - 1).join('::')

            a = cldoc.Page.make_link(l)
            a.addClass('back')

            a.html('<span class="arrow">&crarr;</span>')

            if parts.length == 1
                a.append($('<span>Index</span>'))
            else
                a.append($('<span/>').text(parts[parts.length - 2]))

            div.append(a)

        # Take everything that's not a reference (i.e. everything on this page)
        onpage = page.children()

        for group in cldoc.Node.groups
            @load_group(items, page, onpage.filter(group))

        return $('#cldoc_sidebar_items').children()

    @load_group: (container, page, items) ->
        if items.length == 0
            return

        # Lookup the class representing this type by the tag name of the
        # first element
        ftag = cldoc.tag($(items[0]))[0]
        type = cldoc.Page.node_type(items)

        if !type
            return

        # Add subtitle header for this group
        $('<div class="subtitle"/>').text(type.title[1]).appendTo(container)

        ul = $('<ul/>')
        prev = null

        for item in items
            item = $(item)

            if cldoc.tag(item)[0] != ftag
                tp = cldoc.Page.node_type(item)
            else
                tp = type

            if !tp
                continue

            item = new tp(item)

            if 'render_sidebar' of item
                item.render_sidebar(ul)
                continue

            # Check if we have multiple times the same name for an item.
            # This happens for example for C++ methods with the same name
            # but with different arguments. Those methods are grouped
            # in the sidebar and a counter indicates how many items have
            # the same name
            if prev && prev.name == item.name
                cnt = prev.li.find('.counter')
                cnti = cnt.text()

                if !cnti
                    cnt.text('2')
                else
                    cnt.text(parseInt(cnti) + 1)

                cnt.css('display', 'inline-block')

                continue

            nm = item.sidebar_name()

            if item.ref
                a = $('<a/>', {href: cldoc.Page.make_internal_ref(item.ref)})
            else
                a = $('<a/>', {href: cldoc.Page.make_internal_ref(cldoc.Page.current_page, item.id)})

            a.append(nm)

            li = $('<li/>')

            a.on('click', do (item) =>
                =>

                    if item.ref
                        cldoc.Page.load_ref(item.ref)
                    else
                        cldoc.Page.load(cldoc.Page.current_page, item.id, true)
            )

            prev = {
                'name': item.name,
                'item': item,
                'li': li
            }

            a.append($('<span class="counter"/>'))

            isvirt = item.node.attr('virtual')
            isprot = item.node.attr('access') == 'protected'
            isstat = item.node.attr('static')

            if isprot && isvirt
                li.append($('<span class="protected virtual">p&nbsp;v</span>'))
            else if isprot && isstat
                li.append($('<span class="static protected">s&nbsp;p</span>'))
            else if isprot
                li.append($('<span class="protected">p</span>'))
            else if isstat
                li.append($('<span class="static">s</span>'))
            else if isvirt
                li.append($('<span class="virtual">v</span>'))

            li.append(a)

            brief = new cldoc.Doc(item.brief).render()

            if brief
                brief.appendTo(li)

            ul.append(li)

        ul.appendTo(container)

# vi:ts=4:et
