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

        container = Variable.render_container()
        item.append(container)

        for variable in variables
            new Variable($(variable)).render(container)

    render_fields: (item) ->
        # Add fields
        fields = @node.children('field')

        if fields.length == 0
            return

        container = Field.render_container()
        item.append(container)

        for field in fields
            new Field($(field)).render(container)

Node.types.struct = Struct

# vi:ts=4:et
