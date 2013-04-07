class cldoc.Variable extends cldoc.Node
    @title = ['Variable', 'Variables']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

    render: ->
        e = cldoc.html_escape

        ret = '<tr id="' + e(@node.attr('id')) + '">'

        ret += '<td class="variable_name identifier">' + e(@node.attr('name')) + '</td>'
        ret += '<td class="variable_type">' + new cldoc.Type(@node.children('type')).render() + '</td>'
        ret += '<td class="doc">' + cldoc.Doc.either(@node) + '</td>'

        return ret + '</tr>'

cldoc.Node.types.variable = cldoc.Variable

# vi:ts=4:et
