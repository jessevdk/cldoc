class cldoc.Subclass extends cldoc.Node
    @title = ['Subclass', 'Subclasses']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

        @access = @node.attr('access')

    render: ->
        e = cldoc.html_escape

        ret = '<tr id="' + e(@id) + '">'

        access = @access

        if access == 'public'
            access = ''

        ret += '<td class="keyword">' + e(access) + '</td>'
        ret += '<td>' + cldoc.Page.make_link(@ref, @name) + '</td>'
        ret += '<td>' + cldoc.Doc.brief(@node) + '</td>'

cldoc.Node.types.subclass = cldoc.Subclass

# vi:ts=4:et
