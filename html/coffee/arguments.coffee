class cldoc.Arguments extends cldoc.Node
    @title = ['Arguments', 'Arguments']

    constructor: (@node) ->
        super(@node)

    render_sidebar_function: (func) ->
        a = cldoc.Page.make_link(cldoc.Page.current_page + '#' + func.attr('id'), func.attr('name'))
        return '<li>' + a + '</li>'

    render_sidebar: ->
        funcs = @node.children('function')
        ret = ''

        for f in funcs
            ret += @render_sidebar_function($(f))

        return ret

    render_function: (func) ->
        e = doc.html_escape

        ret = '<tr class="title"
                   id="' + e(func.attr('id')) + '">
                 <td class="identifier">' +
                   e(func.attr('name')) +
                '</td>'

        for loc in func.children('location')
            loc = $(loc)

            file = e(loc.attr('file'))
            line = e(loc.attr('line') + ':' + loc.attr('column'))

            ret += '<td>' + file + '</td><td>' + line + '</td>'
            ret += '</tr><tr><td></td>'

        ret += '</tr>'

        undocumented = func.children('undocumented')

        if undocumented.length > 0
            names = ($(x).attr('name') for x in undocumented).join(', ')

            ret += '<tr class="undocumented"><td>Undocumented arguments:</td>' +
                   '<td colspan="2">' + e(names) + '</td></tr>'

        misspelled = func.children('misspelled')

        if misspelled.length > 0
            names = ($(x).attr('name') for x in undocumented).join(', ')

            ret += '<tr class="misspelled"><td>Misspelled arguments:</td>' +
                   '<td colspan="2">' + e(names) + '</td></tr>'

        if func.children('undocumented-return')
            ret += '<tr class="undocumented"><td colspan="3">Undocumented return value</td></tr>'

        return ret

    render: ->
        funcs = @node.children('function')

        c = '<table class="function">';

        for f in funcs
            c += @render_function($(f))

        return c + '</table>'

cldoc.Node.types.arguments = cldoc.Arguments

# vi:ts=4:et
