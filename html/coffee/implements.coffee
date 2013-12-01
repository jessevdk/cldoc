class cldoc.Implements extends cldoc.Node
    @title = ['Implements', 'Implements']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

        @type = @node.children('type')
        @access = @node.attr('access')

        @name = @type.attr('name')

        ref = @type.attr('ref')

        if ref
            @id = ref.replace('#', '+')

    render: ->
        e = cldoc.html_escape

        ret = '<tr id="' + e(@id) + '">'

        access = @access

        if access == 'public'
            access = ''

        type = new cldoc.Type(@type)

        ret += '<td class="keyword">' + e(access) + '</td>'
        ret += '<td>' + type.render() + '</td>'
        ret += '<td>' + cldoc.Doc.brief(@node) + '</td>'

        return ret + '</tr>'

cldoc.Node.types.implements = cldoc.Implements

# vi:ts=4:et
