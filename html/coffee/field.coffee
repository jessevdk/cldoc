class Field extends Node
    @title = ['Field', 'Fields']

    constructor: (@node) ->
        super(@node)

    @render_container: ->
        $('<table class="fields"/>')

    render: (container) ->
        row = $('<tr/>')

        row.attr('id', @node.attr('id'))

        row.append($('<td class="field_name identifier"/>').text(@node.attr('name')))
        row.append($('<td class="field_type"/>').append(new Type(@node.children('type')).render()))

        doctd = $('<td class="doc"/>').appendTo(row)
        doctd.append(Doc.either(@node))

        container.append(row)

Node.types.field = Field

# vi:ts=4:et
