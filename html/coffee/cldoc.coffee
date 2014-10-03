href = document.location.protocol + '//' + document.location.host + document.location.pathname

escapeDiv = document.createElement('div');
escapeElement = document.createTextNode('');
escapeDiv.appendChild(escapeElement);

window.cldoc = $.extend($.extend({
    host: href.substring(0, href.lastIndexOf('/')),
}, (window.cldoc ? {})), {
    tag: (node) ->
        $.map(node, (e) -> e.tagName.toLowerCase())

    startswith: (s, prefix) ->
        s.indexOf(prefix) == 0

    html_escape: (s) ->
        escapeElement.data = s;
        escapeDiv.innerHTML;

    new_timer: ->
        ret = {start: new Date()}

        ret.tick = (s) ->
            end = new Date()
            ret.start = end

        return ret

    xml_attr: (e, a) ->
        return e.getAttribute(a)
})

$(document).ready(->
    cldoc.Doc.init()
    cldoc.Sidebar.init()
    cldoc.Page.route()
)

# vi:ts=4:et
