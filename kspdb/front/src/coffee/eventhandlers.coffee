$(document).on 'click', '.js-action-partmesh', (event)->
    console.log "clicked"
    partId = $(event.currentTarget).attr "data-part"
    $.get "/part_mesh/#{partId}", (data)->
        $('.js-meshdebug').html JSON.stringify(data)
        window.showMesh data
