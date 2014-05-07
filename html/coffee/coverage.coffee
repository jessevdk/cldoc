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

    render_sidebar_type: (type) ->
        typename = type.attr('name')

        cov = @get_coverage(type)
        e = cldoc.html_escape

        if cov.documented == 0 && cov.undocumented == 0
            return

        tt = cov.documented + ' out of ' + cov.total + ' (' + cov.percentage + '%)'

        a = cldoc.Page.make_link(cldoc.Page.current_page + '#' + typename, typename)

        ret = '<li>'

        if cov.undocumented == 0
            ret += '<span class="bullet complete">&#x2713;</span>'
        else
            ret += '<span class="bullet incomplete">&#10007;</span>'

        ret += a + '<div class="brief">' + e(tt) + '</div>'
        return ret + '</li>'

    render_sidebar: ->
        types = @node.children('type')
        ret = ''

        for type in types
            ret += @render_sidebar_type($(type))

        return ret

    render_type: (type) ->
        ret = ''

        typename = type.attr('name')
        cov = @get_coverage(type)

        if cov.documented == 0 && cov.undocumented == 0
            return ret

        e = cldoc.html_escape

        ret += '<h3 id="' + e(typename) + '">' + e(typename + ' (' + cov.percentage + '%)') + '</h3>'
        ret += '<table class="coverage">'

        ret += '<tr><td>Documented:</td><td>' + e(cov.documented) + '</td></tr>'
        ret += '<tr><td>Undocumented:</td><td>' + e(cov.undocumented) + '</td></tr>'

        ret += '</table><table class="undocumented">'

        for undoc in type.children('undocumented')
            undoc = $(undoc)

            ret += '<tr><td>' + e(undoc.attr('id')) + '</td>'

            for loc in undoc.children('location')
                loc = $(loc)

                file = e(loc.attr('file'))
                line = e(loc.attr('line') + ':' + loc.attr('column'))

                ret += '<td>' + file + '</td><td>' + line + '</td>'
                ret += '</tr><td></td>'

        return ret + '</tr></table>'

    render: ->
        types = @node.children('type')
        ret = ''

        for type in types
            ret += @render_type($(type))

        return ret

cldoc.Node.types.coverage = cldoc.Coverage

# vi:ts=4:et
