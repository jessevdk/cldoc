class Function extends Node
    @title = ['Function', 'Functions']

    constructor: (@node) ->
        super(@node)

    render: (container) ->
        div = $('<div class="function"/>').appendTo(container)

        decldiv = $('<div class="declaration"/>').appendTo(div)
        decldiv.attr('id', @id)

        isvirt = @node.attr('virtual')
        isprot = @node.attr('access') == 'protected'

        if isvirt || isprot
            specs = $('<ul class="specifiers"/>').appendTo(decldiv)

            if isprot
                specs.append($('<li>protected</li>'))

            if isvirt
                specs.append($('<li>virtual</li>'))

                if @node.attr('abstract')
                    specs.append($('<li>abstract</li>'))

        # Return type
        ret = @node.children('return')

        if ret.length > 0
            retdiv = $('<div class="return_type"/>').appendTo(decldiv)

            returntype = ret.children('type')
            retdiv.append(new Type(returntype).render())

        table = $('<table class="declaration"/>').appendTo(decldiv)

        row = $('<tr/>').appendTo(table)
        td = $('<td class="identifier"/>').text(@name).appendTo(row)

        $('<td class="open_paren"/>').text('(').appendTo(row)

        args = @node.children('argument')

        argtable = $('<table class="arguments"/>')

        for i in [0..(args.length - 1)] by 1
            if i != 0
                row = $('<tr/>').appendTo(table)
                $('<td colspan="2"/>').appendTo(row)

            arg = $(args[i])
            doc = Doc.either(arg)

            argtype = arg.children('type')

            $('<td class="argumen_type"/>').append(new Type(argtype).render()).appendTo(row)

            name = arg.attr('name')

            if i != args.length - 1
                name += ','

            $('<td class="argument_name"/>').text(name).appendTo(row)

            argtr = $('<tr/>').appendTo(argtable)
            argtr.attr('id', arg.attr('id'))
            $('<td/>').text(arg.attr('name')).appendTo(argtr)
            $('<td/>').html(doc).appendTo(argtr)

        if args.length == 0
            $('<td colspan="2"/>').appendTo(row)

        $('<td class="close_paren"/>').text(')').appendTo(row)

        Doc.either(@node).appendTo(div)
        argtable.appendTo(div)

        retdoc = Doc.either(ret)

        if retdoc.length > 0
            tr = $('<tr class="return"/>').appendTo(argtable)
            $('<td class="keyword">return</td>').appendTo(tr)
            $('<td/>').append(retdoc).appendTo(tr)

Node.types.function = Function
Node.types.method = Function

# vi:ts=4:et
