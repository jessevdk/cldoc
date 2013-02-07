class References extends Node
    @title = ['References', 'References']

    constructor: (@node) ->
        super(@node)

    render_sidebar: (container) ->
        for child in @node.children()
            child = $(child)

            a = Page.make_link(Page.current_page + '#ref-' + child.attr('id'), child.attr('name'))
            $('<li/>').append($('<span class="keyword"/>').text(child.tag()[0])).append(' ').append(a).appendTo(container)

    @render_container: ->
        $('<table class="references"/>')

    render: (container) ->
        for child in @node.children()
            child = $(child)

            kw = $('<span class="keyword"/>').text(child.tag()[0]).append('&nbsp;')
            id = $('<span class="identifier"/>').text(child.attr('id'))

            row = $('<tr/>').append($('<td class="title"/>').append(kw).append(id)).appendTo(container)
            row.attr('id', 'ref-' + child.attr('id'))

            for loc in child.children('location')
                loc = $(loc)

                $('<td/>').text(loc.attr('file')).appendTo(row)
                $('<td/>').text(loc.attr('line') + ':' + loc.attr('column')).appendTo(row)

                row = $('<tr/>').append('<td/>').appendTo(container)

            for tp in child.children('doctype')
                tp = $(tp)

                name = tp.attr('name')
                component = tp.attr('component')

                if component
                    name = name + '.' + component

                refs = ($(x).attr('name') for x in tp.children('ref')).join(', ')
                row = $('<tr class="missing"/>').append($('<td/>').text(name)).append($('<td/>').text(refs)).append('<td/>').appendTo(container)

            row.addClass('last')

Node.types.references = References

# vi:ts=4:et
