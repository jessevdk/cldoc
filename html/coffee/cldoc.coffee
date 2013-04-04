href = document.location.origin + document.location.pathname

window.cldoc = $.extend($.extend({
    host: href.substring(0, href.lastIndexOf('/')),
}, (window.cldoc ? {})), {
    tag: (node) ->
        $.map(node, (e) -> e.tagName.toLowerCase())

    startswith: (s, prefix) ->
        s.indexOf(prefix) == 0
})

$(document).ready(->
    cldoc.Sidebar.init()
    cldoc.Page.route()
)

# vi:ts=4:et
