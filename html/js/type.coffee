class Type extends Node
    constructor: (@node) ->
        super(@node)

        @qualifier = @node.attr('qualifier')
        @size = @node.attr('size')

        @typeparts = []

        subtype = @node.children('type')

        if subtype.length > 0
            @subtype = new Type(subtype)
            @typeparts = @typeparts.concat(@subtype.typeparts)

        if @name
            if @ref
                a = Page.make_link(@ref, @name)
                @typeparts.push(a)
            else
                @typeparts.push($('<span class="name"/>').text(@name))

        if @qualifier
            @typeparts.push($('<span class="qualifier"/>').text(@qualifier))

        if @size
            @typeparts.push($('<span class="array_size"/>').text('[' + @size + ']'))

    render: ->
        ret = $('<span class="type"/>')


        for item in @typeparts
            ret.append(item)

        return ret

Node.types.type = Type

# vi:ts=4:et
