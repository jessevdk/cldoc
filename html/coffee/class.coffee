class Class extends Struct
    @title = 'Classes'

    constructor: (@node) ->
        super(@node)

    @render_container: ->
        $('<div/>', {'class': 'classes'})

Node.types['class'] = Class
Node.types.classtemplate = Class

# vi:ts=4:et
