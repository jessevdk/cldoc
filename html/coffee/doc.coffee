class cldoc.Doc extends cldoc.Node
    @magic_separator = '%~@#~!'

    constructor: (@node) ->
        super(@node)

    @either: (node) ->
        doc = @doc(node)

        if doc
            return doc

        brief = @brief(node)

        if brief
            return brief

        return $()

    @brief: (node) ->
        return new Doc(node.children('brief')).render()

    @doc: (node) ->
        return new Doc(node.children('doc')).render()

    escape: (text) ->
        r = /([*_\\`{}#+-.!\[\]])/g

        return text.replace(r, (m) -> "\\" + m)

    process_markdown: (text) ->
        converter = new Showdown.converter()
        html = converter.makeHtml(text)

        parts = html.split(Doc.magic_separator)
        rethtml = ''

        for i in [0..parts.length-2] by 3
            a = cldoc.Page.make_link(parts[i + 1], parts[i + 2])
            rethtml += parts[i] + a[0].outerHTML

        return rethtml + parts[parts.length - 1]

    process_code: (code) ->
        ret = $('<pre/>')
        container = $('<code/>').appendTo(ret)

        for c in $(code).contents()
            if c.nodeType == document.ELEMENT_NODE
                tag = c.tagName.toLowerCase()

                c = $(c)

                if tag == 'ref'
                    cldoc.Page.make_link(c.attr('ref'), c.attr('name')).appendTo(container)
                else
                    span = $('<span/>').text(c.text()).appendTo(container)
                    span.addClass(tag)
            else
                text = $(c).text()
                container.append(text)

        return ret

    render: ->
        if !@node
            return null

        container = $('<div/>', {'class': cldoc.tag(@node)[0]})

        contents = @node.contents()
        astext = ''

        msep = Doc.magic_separator

        for c in contents
            if c.nodeType == document.ELEMENT_NODE
                tag = c.tagName.toLowerCase()

                if tag == 'ref'
                    # Add markdown link
                    c = $(c)
                    astext += msep + c.attr('ref') + msep + c.text() + msep
                else if tag == 'code'
                    # Do the code!
                    if astext
                        container.append(@process_markdown(astext))
                        astext = ''

                    container.append(@process_code(c))
            else
                astext += $(c).text()

        if astext
            container.append(@process_markdown(astext))

        # Replace reference links with our custom onclick
        for a in container.find('a')
            a = $(a)
            href = a.attr('href')

            if href[0] == '#'
                a.on('click', do (href) ->
                    ->
                        cldoc.Page.load_ref(cldoc.Page.make_external_ref(href))
                        false
                )

        return container

cldoc.Node.types.doc = cldoc.Doc

# vi:ts=4:et
