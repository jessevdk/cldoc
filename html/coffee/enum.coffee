class Enum extends Node
    @title = ['Enum', 'Enumerations']

    constructor: (@node) ->
        super(@node)

    render: (container) ->
        id = $('<span class="identifier"/>').text(@name)

        isprot = @node.attr('access') == 'protected'

        if isprot
            n = 'protected enum'
        else
            n = 'enum'

        sp = $('<span class="keyword"/>').text(n)
        name = $('<div/>').append(sp).append(' ')

        name.attr('id', @id)

        name.append(id)
        container.append(name)

        doc = new Doc(@doc).render()

        if doc
            container.append(doc)
        else
            brief = new Doc(@doc).render()

            if brief
                container.append(brief)

        table = $('<table/>')
        container.append(table)

        for value in @node.children('enumvalue')
            value = $(value)
            row = $('<tr/>')

            nm = $('<td class="name identifier"/>').text(value.attr('name'))
            nm.attr('id', value.attr('id'))

            row.append(nm)
            row.append($('<td class="value"/>').text(value.attr('value')))

            doctd = $('<td class="doc"/>').appendTo(row)
            doctd.append(Doc.either(value))

            table.append(row)

Node.types.enum = Enum

# vi:ts=4:et
