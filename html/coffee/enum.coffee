class cldoc.Enum extends cldoc.Node
    @title = ['Enum', 'Enumerations']

    constructor: (@node) ->
        super(@node)

    render: ->
        e = cldoc.html_escape

        isprot = @node.attr('access') == 'protected'

        if isprot
            n = 'protected enum'
        else
            n = 'enum'

        if @node.attr('class')
            n += ' class'

        if @node.attr('typedef')
            n = 'typedef ' + n

        ret = '<div id="' + e(@id) + '"><span class="keyword">' + e(n) + '</span> '
        ret += '<span class="identifier">'

        if not cldoc.startswith(@name, '(anonymous')
            ret += e(@name)

        ret += '</span></div>'
        ret += cldoc.Doc.either(@node)

        ret += '<table>'

        for value in @node.children('enumvalue')
            value = $(value)

            ret += '<tr id="' + e(value.attr('id')) + '">'
            ret += '<td class="name identifier">' + e(value.attr('name')) + '</td>'
            ret += '<td class="value">' + e(value.attr('value')) + '</td>'
            ret += '<td class="doc">' + cldoc.Doc.either(value) + '</td>'

            ret += '</tr>'

        return ret + '</table>'

cldoc.Node.types.enum = cldoc.Enum

# vi:ts=4:et
