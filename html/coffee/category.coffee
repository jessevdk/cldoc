class cldoc.Category extends cldoc.Node
    @title = ['Category', 'Categories']

    constructor: (@node) ->
        super(@node)

        @full_name_for_display = @name

    render: ->
        ret = '<div class="item">'

        ret += cldoc.Page.make_link(@ref, @name, {'id': @id})
        ret += new cldoc.Doc(@brief).render()

        categories = @node.children('category')

        if categories.length > 0
            ret += '<table class="category">'

            for cat in categories
                cat = $(cat)

                a = cldoc.Page.make_link(cat.attr('ref'), cat.attr('name'))
                doc = cldoc.Doc.either(cat)

                ret += '<tr><td>' + a + '</td><td class="doc">' + doc + '</td></tr>'

            ret += '</table>'

        return ret

cldoc.Node.types.category = cldoc.Category

# vi:ts=4:et
