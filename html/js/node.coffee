class Node
    @types = {}

    @groups = [
        'category',
        'namespace',
        'typedef',
        'struct, class',
        'enum',
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
        $('<div/>', {'class': @name.toLowerCase() + 's'})

    render: (container) ->
        null

# vi:ts=4:et
