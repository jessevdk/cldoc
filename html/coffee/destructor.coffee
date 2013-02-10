class cldoc.Destructor extends cldoc.Method
    @title = ['Destructor', 'Destructors']

    constructor: (@node) ->
        super(@node)

cldoc.Node.types.destructor = cldoc.Destructor

# vi:ts=4:et
