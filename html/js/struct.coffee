class Struct extends Node
    @title = 'Structures'

    constructor: (@node) ->
        super(@node)

    render: (container) ->
        item = $('<div class="item"/>')

        id = $('<span class="identifier"/>').text(@name)
        name = $('<div><span class="keyword">struct</span> </div>')
        name.attr('id', @id)

        name.append(id)
        item.append(name)

        item.append(Doc.either(@node))

        if @ref
            item.append(Page.know_more(@ref))
        else
            @render_fields(item)
            @render_variables(item)

        container.append(item)

    render_variables: (item) ->
        # Add variables
        variables = @node.children('variable')

        if variables.length == 0
            return

        fc = $('<table/>')
        item.append(fc)

        for variable in variables
            variable = $(variable)
            row = $('<tr/>')

            row.attr('id', variable.attr('id'))

            row.append($('<td class="variable_name identifier"/>').text(variable.attr('name')))
            row.append($('<td class="variable_type"/>').append(new Type(variable.children('type')).render()))

            doctd = $('<td class="doc"/>').appendTo(row)
            doctd.append(Doc.either(variable))

            fc.append(row)

    render_fields: (item) ->
        # Add fields
        fields = @node.children('field')

        if fields.length == 0
            return

        fc = $('<table/>')
        item.append(fc)

        for field in fields
            field = $(field)
            row = $('<tr/>')

            row.attr('id', field.attr('id'))

            row.append($('<td class="field_name identifier"/>').text(field.attr('name')))
            row.append($('<td class="field_type"/>').append(new Type(field.children('type')).render()))

            doctd = $('<td class="doc"/>').appendTo(row)
            doctd.append(Doc.either(field))

            fc.append(row)

Node.types.struct = Struct

# vi:ts=4:et
