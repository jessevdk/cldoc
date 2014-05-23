class cldoc.TemplateTypeParameter extends cldoc.Node
    @title = ['Template Parameter', 'Template Parameters']
    @render_container_tag = 'table'

    render: ->
        e = cldoc.html_escape

        name = @name
        def = @node.attr('default')
        tp = @node.children('type')

        ret = '<tr id="' + e(@id) + '">'

        name = ''

        if tp.length > 0
            name += (new cldoc.Type(tp)).render() + ' '

        name += e(@name)

        if def
            name += ' = <span class="constant">' + def + '</span>'

        ret += '<td>' + name + '</td>'
        ret += '<td>' + cldoc.Doc.brief(@node) + '</td>'
        ret += '</tr>'

        return ret

cldoc.Node.types.templatetypeparameter = cldoc.TemplateTypeParameter
cldoc.Node.types.templatenontypeparameter = cldoc.TemplateTypeParameter

# vi:ts=4:et
