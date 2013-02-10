class cldoc.Field extends cldoc.Node
    @title = ['Field', 'Fields']

    constructor: (@node) ->
        super(@node)

    @render_container: ->
        $('<table class="fields"/>')

    render: (container) ->
        row = $('<tr/>')

        row.attr('id', @node.attr('id'))

        row.append($('<td class="field_name identifier"/>').text(@node.attr('name')))
        row.append($('<td class="field_type"/>').append(new cldoc.Type(@node.children('type')).render()))

        doctd = $('<td class="doc"/>').appendTo(row)
        doctd.append(cldoc.Doc.either(@node))

        container.append(row)

cldoc.Node.types.field = cldoc.Field

# vi:ts=4:et
