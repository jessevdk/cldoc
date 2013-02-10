class cldoc.Typedef extends cldoc.Node
    @title = ['Typedef', 'Typedefs']

    constructor: (@node) ->
        super(@node)

    # Renders the typedefs page container
    @render_container: ->
        $('<table class="alt typedefs"/>')

    # Render the typedef
    render: (container) ->
        row = $('<tr class="typedef"/>')
        row.attr('id', @id)

        row.append($('<td class="typedef_name identifier"/>').text(@node.attr('name')))
        row.append($('<td class="typedef_decl keyword">type</td>'))
        row.append($('<td class="typedef_type"/>').append(new cldoc.Type(@node.children('type')).render()))

        container.append(row)

        row = $('<tr class="doc"/>')
        td = $('<td colspan="3"/>').append(cldoc.Doc.either(@node))

        row.append(td)
        container.append(row)

cldoc.Node.types.typedef = cldoc.Typedef

# vi:ts=4:et
