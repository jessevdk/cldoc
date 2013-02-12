window.cldoc = $.extend($.extend({
    host: document.location.href.substring(0, document.location.href.lastIndexOf('/')),
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
