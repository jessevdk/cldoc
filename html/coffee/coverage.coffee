class cldoc.Coverage extends cldoc.Node
    @title = ['Coverage', 'Coverage']

    constructor: (@node) ->
        super(@node)

    get_coverage: (type) ->
        ret = {
            documented: parseInt(type.attr('documented')),
            undocumented: parseInt(type.attr('undocumented')),
        }

        ret.total = ret.documented + ret.undocumented
        ret.percentage = Math.round(100 * ret.documented / ret.total)

        return ret

    render_sidebar_type: (type, container) ->
        typename = type.attr('name')

        cov = @get_coverage(type)

        if cov.documented == 0 && cov.undocumented == 0
            return

        tt = cov.documented + ' out of ' + cov.total + ' (' + cov.percentage + '%)'

        a = cldoc.Page.make_link(cldoc.Page.current_page + '#' + typename, typename)
        li = $('<li/>').appendTo(container)

        if cov.undocumented == 0
            li.append($('<span class="bullet complete"/>').html('&#x2713;'))
        else
            li.append($('<span class="bullet incomplete"/>').html('&#10007;'))

        li.append(a).append($('<div class="brief"/>').text(tt))

    render_sidebar: (container) ->
        types = @node.children('type')

        for type in types
            @render_sidebar_type($(type), container)

    render_type: (type, container) ->
        typename = type.attr('name')
        cov = @get_coverage(type)

        if cov.documented == 0 && cov.undocumented == 0
            return

        h3 = $('<h3/>').text(typename).append(' (' + cov.percentage + '%)').appendTo(container)
        h3.attr('id', typename)

        t = $('<table class="coverage"/>').appendTo(container)

        $('<tr/>').append($('<td>Documented:</td>')).append($('<td/>').text(cov.documented)).appendTo(t)
        $('<tr/>').append($('<td>Undocumented:</td>')).append($('<td/>').text(cov.undocumented)).appendTo(t)

        t = $('<table class="undocumented"/>').appendTo(container)

        for undoc in type.children('undocumented')
            undoc = $(undoc)
            row = $('<tr/>').appendTo(t)

            $('<td/>').text(undoc.attr('id')).appendTo(row)

            for loc in undoc.children('location')
                loc = $(loc)

                $('<td/>').text(loc.attr('file')).appendTo(row)
                $('<td/>').text(loc.attr('line') + ':' + loc.attr('column')).appendTo(row)

                row = $('<tr/>').append('<td/>').appendTo(t)

    render: (container) ->
        types = @node.children('type')

        for type in types
            @render_type($(type), container)

cldoc.Node.types.coverage = cldoc.Coverage

# vi:ts=4:et
