class Category extends Node
    @title = ['Category', 'Categories']

    constructor: (@node) ->
        super(@node)

    render: (container) ->
        div = $('<div class="item"/>')
        container.append(div)

        a = Page.make_link(@ref, @name)
        a.attr('id', @id)

        div.append(a)
        div.append(new Doc(@brief).render())

        categories = @node.children('category')

        if categories.length > 0
            tb = $('<table class="category"/>')

            for cat in categories
                cat = $(cat)

                row = $('<tr/>')
                a = Page.make_link(cat.attr('ref'), cat.attr('name'))
                row.append($('<td/>').append(a))
                row.append($('<td class="doc"/>').append(Doc.either(cat)))
                tb.append(row)

            div.append(tb)

Node.types.category = Category

# vi:ts=4:et
