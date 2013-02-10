class cldoc.Method extends cldoc.Function
    @title = ['Method', 'Methods']

    constructor: (@node) ->
        super(@node)

cldoc.Node.types.method = cldoc.Method

# vi:ts=4:et
