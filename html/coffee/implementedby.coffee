class cldoc.ImplementedBy extends cldoc.Node
    @title = ['Implemented By', 'Implemented By']

    constructor: (@node) ->
        super(@node)

        @access = @node.attr('access')

    @render_container: ->
        $('<table class="implementedby"/>')

    render: (container) ->
        row = $('<tr/>').appendTo(container)

        row.attr('id', @id)

        access = @access

        if access == 'public'
            access = ''

        $('<td class="keyword"/>').text(access).appendTo(row)
        $('<td/>').html(cldoc.Page.make_link(@ref, @name)).appendTo(row)
        $('<td/>').html(cldoc.Doc.brief(@node)).appendTo(row)

cldoc.Node.types.implementedby = cldoc.ImplementedBy

# vi:ts=4:et
