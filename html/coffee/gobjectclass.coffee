class cldoc.GObjectClass extends cldoc.Class
    @title = ['GObject Class', 'GObject Classes']

    constructor: (@node) ->
        super(@node)

        @keyword = 'struct'

cldoc.Node.types['gobject:class'] = cldoc.GObjectClass

# vi:ts=4:et
