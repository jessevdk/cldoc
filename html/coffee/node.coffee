cldoc.Mixin = (base, mixins...) ->
    for mixin in mixins by -1
        base = mixin(base)

    base

class cldoc.Node
    @types = {}

    @groups = [
        'coverage',
        'arguments',
        'references',
        'category',
        'namespace',
        'templatetypeparameter, templatenontypeparameter',
        'base',
        'implements',
        'subclass',
        'implementedby',
        'typedef',
        'class, classtemplate',
        'gobject\\:class',
        'gobject\\:interface',
        'gobject\\:boxed',
        'struct, structtemplate',
        'enum',
        'field, union',
        'variable',
        'gobject\\:property',
        'constructor',
        'destructor',
        'method, methodtemplate',
        'function, functiontemplate',
        'report'
    ]

    @order = {
        'category': 0,
        'namespace': 1,
        'templatetypeparameter': 2,
        'templatenontypeparameter': 2,
        'base': 3,
        'implements': 3,
        'subclass': 4,
        'implementedby': 4,
        'typedef': 5,
        'class': 6,
        'classtemplate': 6,
        'gobjectclass': 6,
        'gobjectinterface': 7,
        'struct': 8,
        'structtemplate': 8,
        'gobjectboxed': 8,
        'enum': 9,
        'enumvalue': 10,
        'field': 11,
        'union': 12,
        'variable': 13,
        'gobjectproperty': 13,
        'constructor': 14,
        'destructor': 15,
        'method': 16,
        'methodtemplate': 16,
        'function': 17,
        'functiontemplate': 17
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

        if @ref && !@id
            @id = @ref.replace('#', '+')

        @brief = @node.children('brief').first()
        @doc = @node.children('doc').first()

    full_name_for_display: ->
        null

    sidebar_name: ->
        @name

    @render_container: ->
        ['<' + @render_container_tag + ' class="' + cldoc.html_escape(@title[1].toLowerCase().replace(/[ ]/g, '_')) + '">', '</' + @render_container_tag + '>']

    render: ->
        null

# vi:ts=4:et
