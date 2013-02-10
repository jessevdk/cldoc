class cldoc.Enum extends cldoc.Node
    @title = ['Enum', 'Enumerations']

    constructor: (@node) ->
        super(@node)

    render: (container) ->
        id = $('<span class="identifier"/>')

        if not cldoc.startswith(@name, '(anonymous')
            id.text(@name)

        isprot = @node.attr('access') == 'protected'

        if isprot
            n = 'protected enum'
        else
            n = 'enum'

        if @node.attr('class')
            n += ' class'

        if @node.attr('typedef')
            n = 'typedef ' + n

        sp = $('<span class="keyword"/>').text(n)
        name = $('<div/>').append(sp).append(' ')

        name.attr('id', @id)

        name.append(id)
        container.append(name)

        doc = new cldoc.Doc(@doc).render()

        if doc
            container.append(doc)
        else
            brief = new cldoc.Doc(@doc).render()

            if brief
                container.append(brief)

        table = $('<table/>')
        container.append(table)

        for value in @node.children('enumvalue')
            value = $(value)
            row = $('<tr/>')
            row.attr('id', value.attr('id'))

            nm = $('<td class="name identifier"/>').text(value.attr('name'))

            row.append(nm)
            row.append($('<td class="value"/>').text(value.attr('value')))

            doctd = $('<td class="doc"/>').appendTo(row)
            doctd.append(cldoc.Doc.either(value))

            table.append(row)

cldoc.Node.types.enum = cldoc.Enum

# vi:ts=4:et
