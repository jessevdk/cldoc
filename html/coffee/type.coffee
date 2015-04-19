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
            @subtype = @append_type(subtype)

        if @node.attr('class') == 'function'
            @typeparts.push('<span class="function-type">')
            @typeparts_text.push('')

            result = @node.children('result').first()
            args = @node.children('arguments').first().children('type')

            @result = @append_type($(result))
            @args = []

            @typeparts.push('<span class="function-qualified">')
            @typeparts_text.push('')

            @append_plain_part('(')
            @append_qualifier()
            @append_plain_part(')')

            @typeparts.push('</span><span class="function-arguments">')
            @typeparts_text.push('')

            @append_plain_part('(')

            for arg, i in args
                if i != 0
                    @append_plain_part(', ')

                @args.push(@append_type($(arg)))

            @append_plain_part(')')

            @typeparts.push('</span></span>')
            @typeparts_text.push('')
        else
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

            @append_qualifier()

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

    append_type: (type) ->
        type = new Type(type)

        @typeparts.push('<span class="sub-type">')
        @typeparts_text.push('')

        @typeparts = @typeparts.concat(type.typeparts)
        @typeparts_text = @typeparts_text.concat(type.typeparts_text)

        @typeparts.push('</span>')
        @typeparts_text.push('')

        return type

    append_plain_part: (text) ->
        @typeparts.push('<span class="plain">' + cldoc.html_escape(text) + '</span>')
        @typeparts_text.push(text)

    append_qualifier: ->
        if @qualifier
            qc = cldoc.html_escape(@qualifier).replace(/const/g, '<span class="keyword">const</span>')
            q = '<span class="qualifier"> ' + qc  + '</span>'

            @typeparts.push(q)
            @typeparts_text.push(@qualifier)


cldoc.Node.types.type = cldoc.Type

# vi:ts=4:et
