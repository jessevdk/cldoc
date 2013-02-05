class Sidebar
    @load: (page) ->
        items = $('#sidebar_items')
        items.empty()

        head = Page.make_header(page)

        if head
            div = $('<div class="back"/>')
            name = $('<div class="name"/>')

            name.append(head)
            div.append(name)
            items.append(div)

            id = page.attr('id')
            parts = id.split('::')

            l = parts.slice(0, parts.length - 1).join('::')

            a = Page.make_link(l)
            a.addClass('back')

            a.html('<span class="arrow">&crarr;</span>')

            if parts.length == 1
                a.append($('<span>Index</span>'))
            else
                a.append($('<span/>').text(parts[parts.length - 2]))

            div.append(a)

        # Take everything that's not a reference (i.e. everything on this page)
        onpage = page.children().filter(':not([access]), [access=protected], [access=public]')

        for group in Node.groups
            @load_group(page, onpage.filter(group))

    @load_group: (page, items) ->
        container = $('#sidebar_items')

        if items.length != 0
            # Lookup the class representing this type by the tag name of the
            # first element
            typename = items.tag()[0]

            if !(typename of Node.types)
                return

            type = Node.types[typename]

            # Add subtitle header for this group
            $('<div class="subtitle"/>').text(type.title).appendTo(container)

            ul = $('<ul/>')
            prev = null

            for item in items
                item = new type($(item))

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

                a = $('<a/>', {href: Page.make_internal_ref(Page.current_page, item.id)}).text(item.name)
                li = $('<li/>')

                a.on('click', do (item) =>
                    =>
                        Page.load(Page.current_page, item.id, true)
                        false
                )

                prev = {
                    'name': item.name,
                    'item': item,
                    'li': li
                }

                a.append($('<span class="counter"/>'))
                li.append(a)

                brief = new Doc(item.brief).render()

                if brief
                    brief.appendTo(li)

                ul.append(li)

            ul.appendTo(container)

# vi:ts=4:et
