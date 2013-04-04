class cldoc.Type extends cldoc.Node
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
                a = cldoc.Page.make_link(@ref, @name)
                name = $('<span class="name"/>').append(a)
            else
                name =$('<span class="name"/>').text(@name)

            if @node.attr('builtin')
                name.addClass('builtin')

            @typeparts.push(name)

        if @qualifier
            @typeparts.push($('<span class="qualifier"/>').text(' ' + @qualifier + ' '))

        if @size
            @typeparts.push($('<span class="array_size"/>').text('[' + @size + ']'))

    render: ->
        ret = $('<span class="type"/>')

        for item in @typeparts
            ret.append(item)

        return ret

cldoc.Node.types.type = cldoc.Type

# vi:ts=4:et
