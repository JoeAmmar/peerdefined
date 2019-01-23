

// glyphiconArrow = document.querySelectorAll(".glyphicon-up-down");

window.onload = function() {
   $('.big-checkbox').prop('checked', false);
  objects = document.querySelectorAll(".showhide")
  for (var i = 0; i < objects.length; i++) {

    var exp1 = objects[i].getElementsByClassName("expanding")[0];
    var exp2 = objects[i].getElementsByClassName("expanding2")[0];
    var inText = objects[i].getElementsByClassName("in-text")[0];
    var authorsLabel = objects[i].getElementsByClassName("authorsLabel")[0];

    exp1.style.display = "none";
    exp2.style.display = "none";
    if (inText != null){
    inText.style.fontSize = "0px"
  }
}
document.getElementsByClassName("hide-until-load")[0].style.visibility = "visible";
}

function expandBox(obj) {

objects = document.querySelectorAll(".showhide")
for (var i = 0; i < objects.length; i++) {
  if (obj === objects[i].getElementsByClassName("glyphicon-up-down")[0]){
  var exp1 = objects[i].getElementsByClassName("expanding")[0];
  var exp2 = objects[i].getElementsByClassName("expanding2")[0];
  var inText = objects[i].getElementsByClassName("in-text")[0];
  var glyphiconUpDown = objects[i].getElementsByClassName("glyphicon-up-down")[0];
  var authorsLabel = objects[i].getElementsByClassName("authorsLabel")[0];
  if (exp1.style.display === "none") {
        exp1.style.display = "block";
        exp2.style.display = "block";
        if (authorsLabel != null){
        authorsLabel.style.fontSize = "14px";
        authorsLabel.classList.remove('authorsLabelHidden');
      }
        glyphiconUpDown.classList.remove('glyphicon-menu-down');
        glyphiconUpDown.classList.add('glyphicon-menu-up');
        if (inText != null){
          inText.style.fontSize = "14px"
        }
    } else {
        exp1.style.display = "none";
        exp2.style.display = "none";
        glyphiconUpDown.classList.remove('glyphicon-menu-up');
        glyphiconUpDown.classList.add('glyphicon-menu-down');
        if (inText != null){
        inText.style.fontSize = "0px"
      }
        if (authorsLabel != null){
        authorsLabel.classList.add('authorsLabelHidden');
        authorsLabel.style.fontSize = "0px";
      }
    }}};
}
