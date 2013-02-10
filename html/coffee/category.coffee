class cldoc.Category extends cldoc.Node
    @title = ['Category', 'Categories']

    constructor: (@node) ->
        super(@node)

    render: (container) ->
        div = $('<div class="item"/>')
        container.append(div)

        a = cldoc.Page.make_link(@ref, @name)
        a.attr('id', @id)

        div.append(a)
        div.append(new cldoc.Doc(@brief).render())

        categories = @node.children('category')

        if categories.length > 0
            tb = $('<table class="category"/>')

            for cat in categories
                cat = $(cat)

                row = $('<tr/>')
                a = cldoc.Page.make_link(cat.attr('ref'), cat.attr('name'))
                row.append($('<td/>').append(a))
                row.append($('<td class="doc"/>').append(cldoc.Doc.either(cat)))
                tb.append(row)

            div.append(tb)

cldoc.Node.types.category = cldoc.Category

# vi:ts=4:et
