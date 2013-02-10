class cldoc.Subclass extends cldoc.Node
    @title = ['Subclass', 'Subclasses']

    constructor: (@node) ->
        super(@node)

        @access = @node.attr('access')

    @render_container: ->
        $('<table class="subclasses"/>')

    render: (container) ->
        row = $('<tr/>').appendTo(container)

        row.attr('id', @id)

        $('<td class="keyword"/>').text(@access).appendTo(row)
        $('<td/>').html(cldoc.Page.make_link(@ref, @name)).appendTo(row)
        $('<td/>').html(cldoc.Doc.brief(@node)).appendTo(row)

cldoc.Node.types.subclass = cldoc.Subclass

# vi:ts=4:et
