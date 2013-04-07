class cldoc.References extends cldoc.Node
    @title = ['References', 'References']
    @render_container_tag = 'table'

    constructor: (@node) ->
        super(@node)

    render_sidebar: ->
        ret = ''
        e = cldoc.html_escape

        for child in @node.children()
            child = $(child)

            a = cldoc.Page.make_link(cldoc.Page.current_page + '#ref-' + child.attr('id'), child.attr('name'))
            ret += '<li><span class="keyword">' + e(cldoc.tag(child)[0]) + ' ' + a + '</span></li>'

        return ret

    render: ->
        ret = ''
        e = cldoc.html_escape

        for child in @node.children()
            child = $(child)

            kw = '<span class="keyword">' + e(cldoc.tag(child)[0]) + '&nbsp;' + '</span>'
            id = '<span class="identifier">' + e(child.attr('id')) + '</span>'

            ret += '<tr id="' + e('ref-' + child.attr('id')) + '"><td class="title">' + kw + id + '</td>'

            for loc in child.children('location')
                loc = $(loc)

                file = e(loc.attr('file'))
                line = e(loc.attr('line') + ':' + loc.attr('column'))

                ret += '<td>' + file + '</td>'
                ret += '<td>' + line + '</td>'
                ret += '</tr><tr><td></td>'

            ret += '</tr>'

            for tp in child.children('doctype')
                tp = $(tp)

                name = tp.attr('name')
                component = tp.attr('component')

                if component
                    name += '.' + component

                refs = ($(x).attr('name') for x in tp.children('ref')).join(', ')

                ret += '<tr class="missing">'
                ret += '<td>' + e(name) + '</td>'
                ret += '<td>' + e(refs) + '</td>'
                ret += '<td></td>'
                ret += '</tr>'

        return ret

cldoc.Node.types.references = cldoc.References

# vi:ts=4:et
