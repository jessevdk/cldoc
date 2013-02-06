class Arguments extends Node
    @title = ['Arguments', 'Arguments']

    constructor: (@node) ->
        super(@node)

    render_sidebar_function: (func, container) ->
        $('<li/>').text(func.attr('name')).appendTo(container)

    render_sidebar: (container) ->
        funcs = @node.children('function')

        for f in funcs
            @render_sidebar_function($(f), container)

    render_function: (func, container) ->
        $('<tr class="title"/>').append($('<td/>').text(func.attr('name')))
                  .append($('<td/>').text(func.attr('file')))
                  .append($('<td/>').text(func.attr('line') + ':' + func.attr('column')))
                  .appendTo(container)

        undocumented = func.children('undocumented')

        if undocumented.length > 0
            $('<tr class="undocumented"/>').append($('<td/>').text('Undocumented:'))
                      .append($('<td colspan="2"/>').html(['<span class="undocumented">' + $(x).attr('name') + '</span>' for x in undocumented].join(', ')))
                      .appendTo(container)

        misspelled = func.children('misspelled')

        if misspelled.length > 0
            $('<tr class="misspelled"/>').append($('<td/>').text('Misspelled:'))
                      .append($('<td colspan="2"/>').html(['<span class="misspelled">' + $(x).attr('name') + '</span>' for x in misspelled].join(', ')))
                      .appendTo(container)

        if func.children('undocumented-return')
            $('<tr class="undocumented"/>').append($('<td colspan="3"/>').text('Undocumented return value'))
                      .appendTo(container)

    render: (container) ->
        funcs = @node.children('function')
        t = $('<table class="function"/>').appendTo(container)

        for f in funcs
            @render_function($(f), t)

Node.types.arguments = Arguments

# vi:ts=4:et
