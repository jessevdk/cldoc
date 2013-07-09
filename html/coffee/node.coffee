class cldoc.Node
    @types = {}

    @groups = [
        'coverage',
        'arguments',
        'references',
        'category',
        'namespace',
        'base',
        'implements',
        'subclass',
        'implementedby',
        'typedef',
        'class, classtemplate',
        'gobject\\:class',
        'gobject\\:interface',
        'gobject\\:boxed',
        'struct',
        'enum',
        'field, union',
        'variable',
        'gobject\\:property',
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
        'implements': 2,
        'subclass': 3,
        'implementedby': 3,
        'typedef': 4,
        'class': 5,
        'classtemplate': 5,
        'gobjectclass': 5,
        'gobjectinterface': 6,
        'struct': 7,
        'gobjectboxed': 7,
        'enum': 8,
        'enumvalue': 9,
        'field': 10,
        'union': 11,
        'variable': 12,
        'gobjectproperty': 12,
        'constructor': 13,
        'destructor': 14,
        'method': 15,
        'function': 16
    }

    @render_container_tag = 'div'

    constructor: (@node) ->
        if !@node
            return

        if @node.length == 0
            @node = null
            return

        @name = @node.attr('name')
        @id = @node.attr('id')
        @ref = @node.attr('ref')
        @full_name_for_display = null

        if @ref && !@id
            @id = @ref.replace('#', '+')

        @brief = node.children('brief').first()
        @doc = node.children('doc').first()

    sidebar_name: ->
        @name

    @render_container: ->
        ['<' + @render_container_tag + ' class="' + cldoc.html_escape(@title[1].toLowerCase().replace(/[ ]/g, '_')) + '">', '</' + @render_container_tag + '>']

    render: (container) ->
        null

# vi:ts=4:et
