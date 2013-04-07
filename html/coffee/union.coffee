class cldoc.Union extends cldoc.Node
    @title = ['Union', 'Unions']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

    sidebar_name: ->
        e = cldoc.html_escape
        return '<span><span class="keyword">union</span> ' + e(@name) + '</span>'

    render: ->
        ret = '<tr class="union">'

        ret += '<td><span class="keyword">union</span></td>'
        ret += '<td></td>'

        ret += '<td class="doc">' + cldoc.Doc.either(@node) + '</td>'
        ret += '</tr><tr><td colspan="3"><table class="fields union">'

        # Add also the things contained in the union
        for child in @node.children()
            child = $(child)
            tp = cldoc.Page.node_type(child)

            if tp
                ret += new tp(child).render()

        return ret + '</table></td></tr>'

cldoc.Node.types.union = cldoc.Union

# vi:ts=4:et
