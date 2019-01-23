// This function takes an array and returns only unique values
    function unique(arr) {
    var u = {}, a = [];
    for(var i = 0, l = arr.length; i < l; ++i){
        if(!u.hasOwnProperty(arr[i])) {
            a.push(arr[i]);
            u[arr[i]] = 1;
        }
    }
    return a;
}
// Function used to remove citation from listCitations if checkbox unchecked
    Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};


// Main Meat of Function Below

// List of citations initiated outside of function
var listCitations = []
               function citationCheckbox(obj) {
                // get all elements of definitions list
                 var x = document.querySelectorAll(".showhide");

                 for(var i = 0; i<x.length; i++){
                   //Get all tag elements (definitions/synonyms)
                 allTags = x[i].getElementsByClassName("label-as-badge")

                 //Change panel color and up-down arrow color if checkbox checked
                 if(x[i].querySelector('#inlineCheckbox').checked){
                   x[i].classList.remove('panel-primary');
                   x[i].classList.add('panel-warning');
                   x[i].getElementsByClassName("glyphicon-up-down")[0].classList.add('glyphicon-menu-up-down-selected');
                   x[i].getElementsByClassName("glyphicon-up-down")[0].classList.remove('glyphicon-menu-up-down-unselected');

                  // change tag colors if checkbox checked
                  for(var n = 0; n<allTags.length; n++){
                   allTags[n].classList.remove('label-primary');
                   allTags[n].classList.add('label-warning');
                   }

                   // add citation information to listCitations if checkbox checked
                   if (x[i].querySelector('.citation') != null) {
                                        listCitations.push(x[i].querySelector('.citation')['innerText'])
                                      }

                 } else {
                   x[i].classList.add('panel-primary');
                   x[i].classList.remove('panel-warning');
                   if (x[i].querySelector('.citation') != null) {
                     listCitations.remove(x[i].querySelector('.citation')['innerText'])
                   }
                   x[i].getElementsByClassName("glyphicon-up-down")[0].classList.remove('glyphicon-menu-up-down-selected');
                   x[i].getElementsByClassName("glyphicon-up-down")[0].classList.add('glyphicon-menu-up-down-unselected');

                   for(var n = 0; n<allTags.length; n++){
                    allTags[n].classList.add('label-primary');
                    allTags[n].classList.remove('label-warning');
                    }

                 }

                 // Only show unique citations

                listCitations = unique(listCitations)

               }};
