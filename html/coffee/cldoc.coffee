(($) =>
    $.fn.tag = ->
        $.map(this, (e) -> e.tagName.toLowerCase())
)(jQuery)

String.prototype.startswith = (prefix) ->
    @indexOf(prefix) != -1

$(document).ready(->
    Page.route()
)

# vi:ts=4:et
