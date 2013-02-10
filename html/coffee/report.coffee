class cldoc.Report extends cldoc.Node
    @title = ['Report', 'Report']

    constructor: (@node) ->
        super(@node)

    render_sidebar: (container) ->
        container.append($('<li/>').append(cldoc.Page.make_link(@ref, @name)))

    render: (container) ->

cldoc.Node.types.report = cldoc.Report

# vi:ts=4:et
