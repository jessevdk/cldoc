class cldoc.Struct extends cldoc.Node
    @title = ['Struct', 'Structures']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

        if @node.attr('typedef')
            @keyword = 'typedef struct'
        else
            @keyword = 'struct'

    render: ->
        if @ref || @node.children('field, method, function').length == 0
            return @render_short()
        else
            return @render_whole()

    render_short: ->
        e = cldoc.html_escape

        ret = '<tr class="short">'

        if @ref
            id = cldoc.Page.make_link(@ref, @name)
        else
            id = '<span class="identifier">' + e(@name) + '</span>'

        ret += '<td>' + id + '</td>'
        ret += '<td>' + cldoc.Doc.brief(@node) + '</td>'

        return ret + '</tr>'

    render_whole: ->
        e = cldoc.html_escape

        ret += '<tr class="full"><td colspan="2"><div class="item">'

        id = '<span class="identifier">' + e(@name) + '</span>'
        k = '<span class="keyword">'

        isprot = @node.attr('access') == 'protected'

        if isprot
            k += 'protected '

        k += e(@keyword) + '</span>'

        ret += '<div id="' + e(@id) + '">' + k + ' ' + id

        templatetypes = @node.children('templatetypeparameter')

        if templatetypes.length > 0
            ret += '&lt;'

            for t in templatetypes
                t = $(t)

                ret += e(t.attr('name'))

            ret += '&gt;'

        ret += '</div>'
        ret += cldoc.Doc.either(@node)

        ret += @render_fields()
        ret += @render_variables()

        return ret + '</div></td></tr>'

    render_variables: ->
        # Add variables
        variables = @node.children('variable')

        if variables.length == 0
            return ''

        container = cldoc.Variable.render_container()
        itemsc = ''

        for variable in variables
            itemsc += new cldoc.Variable($(variable)).render()

        return container[0] + itemsc + container[1]

    render_fields: ->
        # Add fields
        fields = @node.children('field,union')

        if fields.length == 0
            return ''

        container = cldoc.Field.render_container()
        itemsc = ''

        for field in fields
            field = $(field)

            tp = cldoc.Page.node_type(field)

            if tp
                itemsc += new tp(field).render()

        return container[0] + itemsc + container[1]

cldoc.Node.types.struct = cldoc.Struct

# vi:ts=4:et
