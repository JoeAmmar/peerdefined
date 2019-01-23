// DefinitionsList Function For Copying Apa Citation Information
function citationClipboardFunction(obj){
  citationText = ""
  // Make citations in alphabetical order of first author
  listCitations = listCitations.sort()

  // Creating an off-screen text-box to insert and copy citation information
  // This roundabout method is applied due to security features of certain browsers
  var textarea = document.createElement('textarea');
  textarea.setAttribute('class', 'offscreen');

  //Adding whitespace between citations if there are more than one
  for(var i = 0, l = listCitations.length; i < l; ++i){
  if (i == listCitations.length-1) {
    citationText = citationText+listCitations[i]
  } else{
    citationText = citationText+listCitations[i]+'\n' + '\n'
  }}
  //If there are any citations selected, make the text content of textarea = citationText
  if (citationText.length != 0) {
  textarea.textContent = citationText;
  //actually add the newly created text-box to the html document
  document.body.appendChild(textarea);
  //select and copy information
  textarea.select();
  document.execCommand('copy');

//success izitoast pop-up 1 author
if (listCitations.length === 1) {
  iziToast.show({
      title: 'Success!',
      message: 'Apa style citation copied!',
      color: 'green',
      position: 'topRight',
      timeout: 1500
  });
  //success izitoast pop-up more than 1 author
} else {
  iziToast.show({
      title: 'Success!',
      message: 'Apa style citations copied!',
      color: 'green',
      position: 'topRight',
      timeout: 2000
  });
}
//failed izitoast pop-up
} else{
  iziToast.show({
      title: 'Error',
      message: 'Please select at least one definition.',
      color: 'red',
      position: 'topRight',
      timeout: 2500
  });
}


}
