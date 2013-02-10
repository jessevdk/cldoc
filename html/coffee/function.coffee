class cldoc.Function extends cldoc.Node
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
                specs.append($('<li class="protected">protected</li>'))

            if isvirt
                isover = @node.attr('override')

                if isover
                    specs.append($('<li class="override">override</li>'))
                else
                    specs.append($('<li class="virtual">virtual</li>'))

                if @node.attr('abstract')
                    specs.append($('<li class="abstract">abstract</li>'))

        # Return type
        ret = @node.children('return')

        if ret.length > 0
            retdiv = $('<div class="return_type"/>').appendTo(decldiv)

            returntype = ret.children('type')
            retdiv.append(new cldoc.Type(returntype).render())

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
            doc = cldoc.Doc.either(arg)

            argtype = arg.children('type')

            $('<td class="argumen_type"/>').append(new cldoc.Type(argtype).render()).appendTo(row)

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

        cldoc.Doc.either(@node).appendTo(div)
        argtable.appendTo(div)

        retdoc = cldoc.Doc.either(ret)

        if retdoc.length > 0
            tr = $('<tr class="return"/>').appendTo(argtable)
            $('<td class="keyword">return</td>').appendTo(tr)
            $('<td/>').append(retdoc).appendTo(tr)

        override = @node.children('override')

        if override.length > 0
            overrides = $('<div class="overrides"/>').append($('<span class="title">Overrides: </span>'))
            div.append(overrides)

            for i in [0..override.length-1]
                ov = $(override[i])

                if i != 0
                    if i == override.length - 1
                        overrides.append(' and ')
                    else
                        overrides.append(', ')

                overrides.append(cldoc.Page.make_link(ov.attr('ref'), ov.attr('name')))

cldoc.Node.types.function = cldoc.Function

# vi:ts=4:et
