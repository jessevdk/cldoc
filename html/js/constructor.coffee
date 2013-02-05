class Constructor extends Function
    @title = 'Constructors'

    constructor: (@node) ->
        super(@node)

Node.types.constructor = Constructor

# vi:ts=4:et
