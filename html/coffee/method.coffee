class Method extends Function
    @title = ['Method', 'Methods']

    constructor: (@node) ->
        super(@node)

Node.types.method = Method

# vi:ts=4:et
