class cldoc.Variable extends cldoc.Node
    @title = ['Variable', 'Variables']

    constructor: (@node) ->
        super(@node)

    @render_container: ->
        $('<table class="variables"/>')

    render: (container) ->
        row = $('<tr/>')

        row.attr('id', @node.attr('id'))

        row.append($('<td class="variable_name identifier"/>').text(@node.attr('name')))
        row.append($('<td class="variable_type"/>').append(new cldoc.Type(@node.children('type')).render()))

        doctd = $('<td class="doc"/>').appendTo(row)
        doctd.append(cldoc.Doc.either(@node))

        container.append(row)

cldoc.Node.types.variable = cldoc.Variable

# vi:ts=4:et
