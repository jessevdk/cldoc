class cldoc.Union extends cldoc.Node
    @title = ['Union', 'Unions']

    constructor: (@node) ->
        super(@node)

    @render_container: ->
        $('<table class="fields"/>')

    sidebar_name: ->
        $('<span><span class="keyword">union</span></span>').text(@name)

    render: (container) ->
        row = $('<tr class="union"/>').appendTo(container)
        kw = $('<span class="keyword">union</span>')
        $('<td/>').append(kw).appendTo(row)
        $('<td/>').appendTo(row)

        doctd = $('<td class="doc"/>').appendTo(row)
        doctd.append(cldoc.Doc.either(@node))

        ctable = $('<table class="fields union"/>')
        row = $('<tr/>').appendTo(container)
        td = $('<td colspan="3"/>').appendTo(row).append(ctable)

        # Add also the things contained in the union
        for child in @node.children()
            child = $(child)
            tp = cldoc.Page.node_type(child)

            if tp
                new tp(child).render(ctable)

cldoc.Node.types.union = cldoc.Union

# vi:ts=4:et
