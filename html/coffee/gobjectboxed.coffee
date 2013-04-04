class cldoc.GObjectBoxed extends cldoc.Struct
    @title = ['GObject Boxed Structure', 'GObject Boxed Structures']

    constructor: (@node) ->
        super(@node)

        @keyword = 'struct'

cldoc.Node.types['gobject:boxed'] = cldoc.GObjectBoxed

# vi:ts=4:et
