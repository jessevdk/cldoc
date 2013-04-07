class cldoc.GObjectProperty extends cldoc.Node
    @title = ['GObject Property', 'GObject Properties']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

    render: ->
        e = cldoc.html_escape

        ret  = '<tr id="' + @node.attr('id') + '">'
        ret += '<td class="gobject_property_name identifier">' + e(@node.attr('name')) + '</td>'

        mode = @node.attr('mode')
        ret += '<td class="gobject_property_mode">'

        if mode
            ret += '<ul class="gobject_property_mode">'

            for x in mode.split(',')
                ret += '<li class="keyword">' + e(x) + '</li>'

            ret += '</ul>'

        ret += '<td class="gobject_property_type">' + new cldoc.Type(@node.children('type')).render() + '</td>'
        ret += '<td class="doc">' + cldoc.Doc.either(@node) + '</td>'

        return ret + '</tr>'

cldoc.Node.types['gobject:property'] = cldoc.GObjectProperty

# vi:ts=4:et
