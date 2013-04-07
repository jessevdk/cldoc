class cldoc.Namespace extends cldoc.Node
    @title = ['Namespace', 'Namespaces']

    constructor: (@node) ->
        super(@node)

    render: ->
        ret = '<div class="item">'

        ret += cldoc.Page.make_link(@ref, @name, {'id': @id})
        ret += new cldoc.Doc(@brief).render()

        classes = @node.children('class,struct')

        if classes.length > 0
            ret += '<table class="namespace">'

            for cls in classes
                cls = $(cls)

                ret += '<tr>'

                a = cldoc.Page.make_link(cls.attr('ref'), cls.attr('name'))

                ret += '<td>' + a + '</td>'
                ret += '<td class="doc">' + cldoc.Doc.either(cls) + '</td>'

                ret += '</tr>'

            ret += '</table>'

        return ret

cldoc.Node.types.namespace = cldoc.Namespace

# vi:ts=4:et
