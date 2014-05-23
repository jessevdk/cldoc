class cldoc.Type extends cldoc.Node
    constructor: (@node) ->
        super(@node)

        @qualifier = @node.attr('qualifier')
        @size = @node.attr('size')
        @transfer_ownership = @node.attr('transfer-ownership') or 'none'
        @allow_none = @node.attr('allow-none') == 'yes'

        @typeparts = []
        @typeparts_text = []

        subtype = @node.children('type')
        e = cldoc.html_escape

        if subtype.length > 0
            @subtype = new Type(subtype)
            @typeparts = @typeparts.concat(@subtype.typeparts)
            @typeparts_text = @typeparts_text.contact(@subtype.typeparts_text)

        if @name
            if @node.attr('builtin')
                builtincls = 'builtin'
            else
                builtincls = ''

            if @ref
                a = cldoc.Page.make_link(@ref, @name)

                name = '<span class="name ' + builtincls + '">' + a + '</span>'
            else
                name = '<span class="name ' + builtincls + '">' + e(@name) + '</span>'

            @typeparts.push(name)
            @typeparts_text.push(@name)

        if @qualifier
            qc = e(@qualifier).replace(/const/g, '<span class="keyword">const</span>')
            q = '<span class="qualifier"> ' + qc  + '</span>'

            @typeparts.push('<span class="qualifier">' + q + '</span>')
            @typeparts_text.push(@qualifier)

        if @size
            @typeparts.push('<span class="array_size">' + '[' + @size + ']' + '</span>')
            @typeparts_text.push('[' + @size + ']')

    as_text: ->
        @typeparts_text.join('')

    render: ->
        ret = '<span class="type">'

        for item in @typeparts
            ret += item

        return ret

cldoc.Node.types.type = cldoc.Type

# vi:ts=4:et
