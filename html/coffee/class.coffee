class cldoc.Class extends cldoc.Struct
    @title = ['Class', 'Classes']

    constructor: (@node) ->
        super(@node)

        @keyword = 'class'

cldoc.Node.types['class'] = cldoc.Class
cldoc.Node.types.classtemplate = cldoc.Class

# vi:ts=4:et
