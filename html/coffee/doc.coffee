class Doc extends Node
    constructor: (@node) ->
        super(@node)

    @either: (node) ->
        doc = new Doc(node.children('doc')).render()

        if doc
            return doc

        brief = new Doc(node.children('brief')).render()

        if brief
            return brief

        return $()

    escape: (text) ->
        r = /([*_\\`{}#+-.!\[\]])/

        return text.replace(r, (m) -> "\\" + m)

    render: ->
        if !@node
            return null

        contents = @node.contents()
        ret = ''

        for c in contents
            if c.nodeType == document.ELEMENT_NODE and c.tagName.toLowerCase() == 'ref'
                # Add markdown link
                c = $(c)

                iref = Page.make_internal_ref(c.attr('ref'))
                ret += '[' + @escape(c.text()) + '](' + iref + ')'
            else
                ret += $(c).text()

        text = ret.trim()
        ret = $('<div/>', {'class': @node.tag()})

        converter = new Showdown.converter()
        ret.html(converter.makeHtml(text))

        # Replace reference links with our custom onclick
        for a in ret.find('a')
            a = $(a)
            href = a.attr('href')

            if href[0] == '#'
                a.on('click', do (href) ->
                    ->
                        Page.load_ref(Page.make_external_ref(href))
                        false
                )

        return ret

Node.types.doc = Doc

# vi:ts=4:et
