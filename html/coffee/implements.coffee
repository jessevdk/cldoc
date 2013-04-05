class cldoc.Implements extends cldoc.Node
    @title = ['Implements', 'Implements']

    constructor: (@node) ->
        super(@node)

        @type = @node.children('type')
        @access = @node.attr('access')

        @name = @type.attr('name')
        @id = @type.attr('ref')

    @render_container: ->
        $('<table class="implements"/>')

    render: (container) ->
        type = new cldoc.Type(@type)

        row = $('<tr/>').appendTo(container)
        row.attr('id', @id)

        access = @access

        if access == 'public'
            access = ''

        $('<td class="keyword"/>').text(access).appendTo(row)
        $('<td/>').html(type.render()).appendTo(row)
        $('<td/>').html(cldoc.Doc.brief(@node)).appendTo(row)

cldoc.Node.types.implements = cldoc.Implements

# vi:ts=4:et
