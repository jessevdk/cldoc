class cldoc.GObjectInterface extends cldoc.Class
    @title = ['GObject Interface', 'GObject Interfaces']

    constructor: (@node) ->
        super(@node)

        @keyword = 'interface'

cldoc.Node.types['gobject:interface'] = cldoc.GObjectInterface

# vi:ts=4:et
