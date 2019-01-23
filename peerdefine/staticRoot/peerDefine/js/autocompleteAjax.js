
  $(function() {
    $("#terms").autocomplete({
      source: "/api/get_terms/",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 3,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
    return false;
  }
