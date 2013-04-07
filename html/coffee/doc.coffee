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

        return ''

    @brief: (node) ->
        return new Doc(node.children('brief')).render()

    @doc: (node) ->
        return new Doc(node.children('doc')).render()

    escape: (text) ->
        r = /([*_\\`{}#+-.!\[\]])/g

        return text.replace(r, (m) -> "\\" + m)

    process_markdown: (text) ->
        html = marked(text)

        parts = html.split(Doc.magic_separator)
        rethtml = ''

        for i in [0..parts.length-2] by 3
            a = cldoc.Page.make_link(parts[i + 1], parts[i + 2])
            rethtml += parts[i] + a

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
            return ''

        e = cldoc.html_escape
        ret = '<div class="' + e(cldoc.tag(@node)[0]) + '">'

        contents = @node.contents()
        astext = ''

        msep = Doc.magic_separator

        for c in contents
            if c.nodeType == document.ELEMENT_NODE
                tag = c.tagName.toLowerCase()

                if tag == 'ref'
                    # Add markdown link
                    c = $(c)
                    astext += @escape(msep + c.attr('ref') + msep + c.text() + msep)
                else if tag == 'code'
                    # Do the code!
                    if astext
                        ret += @process_markdown(astext)
                        astext = ''

                    ret += @process_code(c)
            else
                astext += $(c).text()

        if astext
            ret += @process_markdown(astext)

        return ret + '</div>'

cldoc.Node.types.doc = cldoc.Doc

# vi:ts=4:et
