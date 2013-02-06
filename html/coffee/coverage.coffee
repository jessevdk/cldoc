class Coverage extends Node
    @title = ['Coverage', 'Coverage']

    constructor: (@node) ->
        super(@node)

    render_sidebar_type: (type, container) ->
        typename = type.attr('name')

        documented = parseInt(type.attr('documented'))
        undocumented = parseInt(type.attr('undocumented'))

        if documented == 0 && undocumented == 0
            return

        cov = Math.round(100 * (documented / (documented + undocumented)))

        t = typename + ' (' + cov + '%)'
        $('<li/>').text(t).appendTo(container)

    render_sidebar: (container) ->
        types = @node.children('type')

        for type in types
            @render_sidebar_type($(type), container)

    render_type: (type, container) ->
        typename = type.attr('name')

        documented = parseInt(type.attr('documented'))
        undocumented = parseInt(type.attr('undocumented'))

        if documented == 0 && undocumented == 0
            return

        cov = Math.round(100 * (documented / (documented + undocumented)))

        $('<h3/>').text(typename).append(' (' + cov + '%)').appendTo(container)
        t = $('<table class="coverage"/>').appendTo(container)

        $('<tr/>').append($('<td>Documented:</td>')).append($('<td/>').text(documented)).appendTo(t)
        $('<tr/>').append($('<td>Undocumented:</td>')).append($('<td/>').text(undocumented)).appendTo(t)

        t = $('<table class="undocumented"/>').appendTo(container)

        for undoc in type.children('undocumented')
            undoc = $(undoc)
            row = $('<tr/>').appendTo(t)

            $('<td/>').text(undoc.attr('id')).appendTo(row)
            $('<td/>').text(undoc.attr('file')).appendTo(row)
            $('<td/>').text(undoc.attr('line') + ':' + undoc.attr('column')).appendTo(row)

    render: (container) ->
        types = @node.children('type')

        for type in types
            @render_type($(type), container)

Node.types.coverage = Coverage

# vi:ts=4:et
