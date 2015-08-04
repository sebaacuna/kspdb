(function() {
  $(document).on('click', '.js-action-partmesh', function(event) {
    var partId;
    console.log("clicked");
    partId = $(event.currentTarget).attr("data-part");
    return $.get("/part_mesh/" + partId, function(data) {
      $('.js-meshdebug').html(JSON.stringify(data));
      return window.showMesh(data);
    });
  });

}).call(this);
