class Node
    @types = {}

    @groups = [
        'category',
        'namespace',
        'typedef',
        'class, classtemplate',
        'struct',
        'enum',
        'field',
        'variable',
        'constructor',
        'method, function',
    ]

    constructor: (@node) ->
        if !@node
            return

        if @node.length == 0
            @node = null
            return

        @name = @node.attr('name')
        @id = @node.attr('id')
        @ref = @node.attr('ref')

        if @ref && !@id
            @id = @ref.replace('#', '+')

        @brief = node.children('brief').first()
        @doc = node.children('doc').first()

    @render_container: ->
        $('<div/>', {'class': @title[1].toLowerCase()})

    render: (container) ->
        null

# vi:ts=4:et
