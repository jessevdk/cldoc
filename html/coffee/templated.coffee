cldoc.Templated = (base) ->
    class MixedIn extends base
        template_parameter_name: (param) ->
            param = $(param)

            name = param.attr('name')
            def = param.attr('default')
            tp = param.children('type')

            ret = ''

            if tp.length > 0
                ret += (new cldoc.Type(tp)).as_text() + ' '

            ret += name

            if def
                ret += ' = ' + def

            return ret

        templated_name: ->
            name = @name

            name += '<'
            name += (@template_parameter_name(x) for x in @node.children('templatetypeparameter, templatenontypeparameter')).join(', ')
            name += '>'

            return name

        identifier_for_display: ->
            @templated_name()

        full_name_for_display: ->
            @templated_name()

        sidebar_name: ->
            @identifier_for_display()

        render_arguments: ->
            ret = '<table class="function-template-parameters">'
            tt = @node.children('templatetypeparameter, templatenontypeparameter')

            for x in tt
                x = $(x)

                ret += '<tr>'
                ret += '<td>' + x.attr('name') + '</td>'
                ret += '<td>' + cldoc.Doc.either(x) + '</td>'
                ret += '</tr>'

            ret += '</table>'

            ret += super

            return ret

    MixedIn

# vi:ts=4:et
