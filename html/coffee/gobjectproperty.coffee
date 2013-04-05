class cldoc.GObjectProperty extends cldoc.Node
    @title = ['GObject Property', 'GObject Properties']

    constructor: (@node) ->
        super(@node)

    @render_container: ->
        $('<table class="gobject_properties"/>')

    render: (container) ->
        row = $('<tr/>')

        row.attr('id', @node.attr('id'))

        row.append($('<td class="gobject_property_name identifier"/>').text(@node.attr('name')))

        mode = @node.attr('mode')
        tdmode = $('<td class="gobject_property_mode"/>')

        if mode
            ul = $('<ul class="gobject_property_mode"/>')
            ul.append($('<li class="keyword"/>').text(x)) for x in mode.split(',')
            tdmode.append(ul)

        row.append(tdmode)
        row.append($('<td class="gobject_property_type"/>').append(new cldoc.Type(@node.children('type')).render()))

        doctd = $('<td class="doc"/>').appendTo(row)
        doctd.append(cldoc.Doc.either(@node))

        container.append(row)

cldoc.Node.types['gobject:property'] = cldoc.GObjectProperty

# vi:ts=4:et
