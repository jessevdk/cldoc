window.cldoc = $.extend($.extend({
    host: document.location.origin + '/' + document.location.pathname.substring(0, document.location.pathname.lastIndexOf('/')),
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
