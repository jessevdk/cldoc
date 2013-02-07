class Report extends Node
    @title = ['Report', 'Report']

    constructor: (@node) ->
        super(@node)

    render_sidebar: (container) ->
        container.append($('<li/>').append(Page.make_link(@ref, @name)))

    render: (container) ->

Node.types.report = Report

# vi:ts=4:et
