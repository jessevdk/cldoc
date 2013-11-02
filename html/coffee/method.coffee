class cldoc.Method extends cldoc.Function
    @title = ['Member Function', 'Member Functions']

    constructor: (@node) ->
        super(@node)

cldoc.Node.types.method = cldoc.Method

# vi:ts=4:et
