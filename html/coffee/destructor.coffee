class Destructor extends Method
    @title = ['Destructor', 'Destructors']

    constructor: (@node) ->
        super(@node)

Node.types.destructor = Destructor

# vi:ts=4:et
