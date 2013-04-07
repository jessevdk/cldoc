class cldoc.Typedef extends cldoc.Node
    @title = ['Typedef', 'Typedefs']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

    # Render the typedef
    render: ->
        e = cldoc.html_escape

        ret = '<tr class="typedef" id="' + e(@id) + '">'

        ret += '<td class="typedef_name identifier">' + e(@node.attr('name')) + '</td>'
        ret += '<td class="typedef_decl keyword">type</td>'
        ret += '<td class="typedef_type">' + new cldoc.Type(@node.children('type')).render() + '</td>'

        ret += '</tr>'

        ret += '<tr class="doc">'
        ret += '<td colspan="3">' + cldoc.Doc.either(@node) + '</td>'

        return ret + '</tr>'

cldoc.Node.types.typedef = cldoc.Typedef

# vi:ts=4:et
