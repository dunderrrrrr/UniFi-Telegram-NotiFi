$(document).ready(function(){
  $("#boxSearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#macbox div.boxer").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
