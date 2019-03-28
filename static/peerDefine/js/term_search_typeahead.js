// used for autocomplete in search bar

$(document).ready(function() {
    $('#term-search').typeahead({source: function (query, process) {
        return $.getJSON(
            '/autocomplete/term_autocomplete/', // this is the url for the created view
             { query : query },
             function (data) {
                //console.log(data) ;
                return process(data);
             });
        }});
 });
