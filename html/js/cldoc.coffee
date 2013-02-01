(($) =>
    $.fn.tag = ->
        $.map(this, (e) -> e.tagName.toLowerCase())

)(jQuery)

$(document).ready(->
    Page.route()
)

# vi:ts=4:et
