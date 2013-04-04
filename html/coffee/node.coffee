class cldoc.Node
    @types = {}

    @groups = [
        'coverage',
        'arguments',
        'references',
        'category',
        'namespace',
        'base',
        'subclass',
        'typedef',
        'class, classtemplate, gobject\\:class',
        'struct, gobject\\:boxed',
        'enum',
        'field, union',
        'variable',
        'constructor',
        'destructor',
        'method',
        'function',
        'report'
    ]

    @order = {
        'category': 0,
        'namespace': 1,
        'base': 2,
        'subclass': 3,
        'typedef': 4,
        'class': 5,
        'classtemplate': 5,
        'gobjectclass': 5,
        'struct': 6,
        'gobjectboxed': 6,
        'enum': 7,
        'enumvalue': 8,
        'field': 9,
        'union': 10,
        'variable': 11,
        'constructor': 12,
        'destructor': 13,
        'method': 14,
        'function': 15
    }

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

    sidebar_name: ->
        @name

    @render_container: ->
        $('<div/>', {'class': @title[1].toLowerCase()})

    render: (container) ->
        null

# vi:ts=4:et
