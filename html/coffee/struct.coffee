class cldoc.Struct extends cldoc.Node
    @title = ['Struct', 'Structures']

    constructor: (@node) ->
        super(@node)

        if @node.attr('typedef')
            @keyword = 'typedef struct'
        else
            @keyword = 'struct'

    @render_container: ->
        return $('<table/>', {'class': @title[1].toLowerCase().replace(' ', '_')})

    render: (container) ->
        if @ref || @node.children('field, method, function').length == 0
            @render_short(container)
        else
            @render_whole(container)

    render_short: (container) ->
        row = $('<tr class="short"/>')

        if @ref
            id = cldoc.Page.make_link(@ref, @name)
        else
            id = $('<span class="identifier"/>').text(@name)

        row.append($('<td/>').html(id))
        row.append($('<td/>').html(cldoc.Doc.brief(@node)))

        container.append(row)

    render_whole: (container) ->
        item = $('<div class="item"/>')

        id = $('<span class="identifier"/>').text(@name)
        k = $('<span class="keyword"/>')

        isprot = @node.attr('access') == 'protected'

        if isprot
            k.append('protected ')

        k.append(@keyword)

        name = $('<div/>').append(k).append(' ')
        name.attr('id', @id)

        name.append(id)

        templatetypes = @node.children('templatetypeparameter')

        if templatetypes.length > 0
            name.append('&lt;')

            for t in templatetypes
                t = $(t)
                name.append(t.attr('name'))

            name.append('&gt;')

        item.append(name)
        item.append(cldoc.Doc.either(@node))

        @render_fields(item)
        @render_variables(item)

        row = $('<tr class="full"/>').append($('<td colspan="2"/>').append(item))
        container.append(row)

    render_variables: (item) ->
        # Add variables
        variables = @node.children('variable')

        if variables.length == 0
            return

        container = cldoc.Variable.render_container()
        item.append(container)

        for variable in variables
            new cldoc.Variable($(variable)).render(container)

    render_fields: (item) ->
        # Add fields
        fields = @node.children('field, union')

        if fields.length == 0
            return

        container = cldoc.Field.render_container()
        item.append(container)

        for field in fields
            field = $(field)

            tp = cldoc.Page.node_type(field)

            if tp
                new tp(field).render(container)

cldoc.Node.types.struct = cldoc.Struct

# vi:ts=4:et
