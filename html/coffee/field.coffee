class cldoc.Field extends cldoc.Node
    @title = ['Field', 'Fields']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

    render: ->
        e = cldoc.html_escape
        ret = '<tr id="' + e(@node.attr('id')) + '">'

        ret += '<td class="field_name identifier">' + e(@node.attr('name')) + '</td>'
        ret += '<td class="field_type">' + e(new cldoc.Type(@node.children('type')).render()) + '</td>'
        ret += '<td class="doc">' + cldoc.Doc.either(@node) + '</td>'

        return ret + '</tr>'

cldoc.Node.types.field = cldoc.Field

# vi:ts=4:et
