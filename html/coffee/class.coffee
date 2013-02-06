class Class extends Struct
    @title = ['Class', 'Classes']

    constructor: (@node) ->
        super(@node)

        @keyword = 'class'

Node.types['class'] = Class
Node.types.classtemplate = Class

# vi:ts=4:et
