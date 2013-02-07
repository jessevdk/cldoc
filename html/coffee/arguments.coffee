class Arguments extends Node
    @title = ['Arguments', 'Arguments']

    constructor: (@node) ->
        super(@node)

    render_sidebar_function: (func, container) ->
        a = Page.make_link(Page.current_page + '#' + func.attr('id'), func.attr('name'))

        $('<li/>').html(a).appendTo(container)

    render_sidebar: (container) ->
        funcs = @node.children('function')

        for f in funcs
            @render_sidebar_function($(f), container)

    render_function: (func, container) ->
        row = $('<tr class="title"/>').append($('<td class="identifier"/>').text(func.attr('name'))).appendTo(container)
        row.attr('id', func.attr('id'))

        for loc in func.children('location')
            loc = $(loc)

            $('<td/>').text(loc.attr('file')).appendTo(row)
            $('<td/>').text(loc.attr('line') + ':' + loc.attr('column')).appendTo(row)

            row = $('<tr/>').append('<td/>').appendTo(container)

        undocumented = func.children('undocumented')

        if undocumented.length > 0
            row = $('<tr class="undocumented"/>').append($('<td/>').text('Undocumented arguments:'))
                      .append($('<td colspan="2"/>').html(($(x).attr('name') for x in undocumented).join(', ')))
                      .appendTo(container)

        misspelled = func.children('misspelled')

        if misspelled.length > 0
            row = $('<tr class="misspelled"/>').append($('<td/>').text('Misspelled arguments:'))
                      .append($('<td colspan="2"/>').html(($(x).attr('name') for x in misspelled).join(', ')))
                      .appendTo(container)

        if func.children('undocumented-return')
            row = $('<tr class="undocumented"/>').append($('<td colspan="3"/>').text('Undocumented return value'))
                      .appendTo(container)

        row.addClass('last')

    render: (container) ->
        funcs = @node.children('function')
        t = $('<table class="function"/>').appendTo(container)

        for f in funcs
            @render_function($(f), t)

Node.types.arguments = Arguments

# vi:ts=4:et
