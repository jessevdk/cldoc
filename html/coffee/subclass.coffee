class Subclass extends Node
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
        $('<td/>').html(Page.make_link(@ref, @name)).appendTo(row)
        $('<td/>').html(Doc.brief(@node)).appendTo(row)

Node.types.subclass = Subclass

# vi:ts=4:et
