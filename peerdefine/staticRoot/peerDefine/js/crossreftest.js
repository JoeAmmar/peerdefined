evalTest = $.getJSON("https://api.crossref.org/works?query=10.1016/j.neuropsychologia.2014.08.012&rows=1")
evalClean = JSON.parse(evalTest['responseText'])['message']['items'][0]

authors = evalClean['author']
title = evalClean['title']
containerTitle = evalClean['container-title']
year = evalClean['published-print']['date-parts'][0][0]
publisher = evalClean['publisher']
publishLocation = evalClean['publisher-location']
page = evalClean['page']
doi = evalClean['DOI']
type = evalClean['type']
volume = evalClean['volume']
citations = evalClean['is-referenced-by-count']
journal = evalClean['container-title']


var yearForm = $('#id_year');
yearForm.val(year)


authorsLen = authors.length;
authorList = []
for (var i = 0; i < authorsLen; i++) {
  authConcat = authors[i]['given'] + " " + authors[i]['family']
  authorList.push(authConcat)
};


          var inTextList = ""

          if(authorList.length ==2){
            inTextList += authorList[0].split(" ").last().concat(" & ") +
            authorList[1].split(" ").last().concat(", ")
            inTextList += year
          } else if(authorList.length < 6){
          inTextList += authorList[0].split(" ").last().concat(", ")
          for(var i = 1; i<authorList.length; i++){
          inTextList += authorList[i].split(" ").last().concat(", ") }
          inTextList += year
        } else {
          inTextList += authorList[0].split(" ").last() +
          " et al., " + year
        };
          var inTextForm = $('#id_author-0-in_text');
          inTextForm.val(inTextList)




string = ''
htmlCitation = ''
for(var i = 0; i<authorList.length; i++){
  aut = authorList[i]
    if(authorList.length > 7 && authorList[5] == aut){
        if(aut.split(" ").length == 1){
            string += aut.split(" ").last() + ",..."
        } else if(aut.split(" ").length == 2){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ".,..."
        } else if(aut.split(" ").length == 3){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] +
                ". " + aut.split(" ")[1][0] + ".,..."
        } else if(aut.split(" ").length == 4){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ". " +
                aut.split(" ")[1][0] + ". " +
                aut.split(" ")[2][0] + ".,..."
        } else if(aut.split(" ").length == 5){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ". " + aut.split(
            )[1][0] + ". " + aut.split(" ")[2][0] + ". " + aut.split(" ")[3][0] + ".,..."
          }

        if(authorList.last().split(" ").length == 1){
            string += authorList.last().split(" ").last() + " "
        } else if(authorList.last().split(" ").length == 2){
            string += authorList.last().split(" ").last() + ", " +
                authorList.last().split(" ")[0][0] + ". "
        } else if(authorList.last().split(" ").length == 3 ){
            string += authorList.last().split(" ").last() + ", " + authorList.last().split(" ")[
                0][0] + ". " + authorList.last().split(" ")[1][0] + ". "
        } else if(authorList.last().split(" ").length == 4 ){
            string += authorList.last().split(" ").last() + ", " + authorList.last().split(" ")[0][0] + ". " +
                authorList.last().split(" ")[1][0] + ". " +
                authorList.last().split(" ")[2][0] + ". "
        } else if(authorList.last().split(" ").length == 5 ){
            string += authorList.last().split(" ").last() + ", " + authorList.last().split(" ")[0][0] + ". " + authorList.last().split(" ")[
                1][0] + ". " + authorList.last().split(" ")[2][0] + ". " + authorList.last().split(" ")[3][0] + ". "
            }
        break;
    } else if(authorList.last() != aut || authorList.length == 1){
        if(aut.split(" ").length == 1){
            string += aut.split(" ").last()
      } else if(aut.split(" ").length == 2){
            string += aut.split(" ").last() + ", " +
                aut.split(" ")[0][0] + "."
      } else if(aut.split(" ").length == 3){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] +
                ". " + aut.split(" ")[1][0] + "."
      } else if(aut.split(" ").length == 4){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ". " +
                aut.split(" ")[1][0] + ". " +
                aut.split(" ")[2][0] + "."
      } else if(aut.split(" ").length == 5){
            string += aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ". " + aut.split(
            )[1][0] + ". " + aut.split(" ")[2][0] + ". " + aut.split(" ")[3][0] + "."
          }
      if(authorList.length == 1){
        string += ' '
      } else{
        string += ', '
      }
  } else{
        if(aut.split(" ").length == 1){
            string += "& " + aut.split(" ").last() + " "
      } else if(aut.split(" ").length == 2){
            string += "& " + aut.split(" ").last() + ", " +
                aut.split(" ")[0][0] + ". "
      } else if(aut.split(" ").length == 3){
            string += "& " + aut.split(" ").last() + ", " + aut.split(" ")[0][0] +
                ". " + aut.split(" ")[1][0] + ". "
      } else if(aut.split(" ").length == 4){
            string += "& " + aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ". " +
                aut.split(" ")[1][0] + ". " +
                aut.split(" ")[2][0] + ". "
      } else if(aut.split(" ").length == 5){
            string += "& " + aut.split(" ").last() + ", " + aut.split(" ")[0][0] + ". " + aut.split(
            )[1][0] + ". " + aut.split(" ")[2][0] + ". " + aut.split(" ")[3][0] + ". "
}}};

title = title.toString()
formatTitle = ''
titleChars = title.split("")
titleIndex = -1
if(title.search('\\:') != -1){
    titleIndex = title.search('\\:')}
if(titleIndex != -1){
    if(titleChars[titleIndex + 1] != ' '){
        titleChars[titleIndex + 1] = titleChars[titleIndex + 1].toUpperCase()
    } else if(titleChars[titleIndex + 2] != ' '){
        titleChars[titleIndex + 2] = titleChars[titleIndex + 2].toUpperCase()}};
formatTitle = titleChars.join("")




// Adding title information to citation
htmlCitation = "<p>" + string
if(type == 'book-chapter' || type == 'book'){
string += "(" + year + "). " + formatTitle
htmlCitation += "(" + year + "). " + "<i>" + formatTitle + "</i>"
if(title[-1] != '.'){
    string += '.'
    htmlCitation += '.'
} else{
    string += ''
  }

if(typeof publishLocation !== 'undefined' && publishLocation && (type == 'book-chapter' || type == 'book')){
      string += " " + publishLocation + ": "
      htmlCitation += " " + publishLocation + ": "
    }

if(typeof publisher !== 'undefined' && publisher && (type == 'book-chapter' || type == 'book')){
          string += publisher
          htmlCitation += publisher
        }
if(typeof volume !== 'undefined' && volume){
    string += volume + ', '
    htmlCitation += volume + ', '
  }

if(typeof page !== 'undefined' && page){
    string += page + "."
    htmlCitation += page + "."
  }

if(typeof doi !== 'undefined' && doi && type != 'book-chapter' && type != 'book'){
    string += " doi\:" + doi
    htmlCitation += " doi\:" + doi
  }
} else{
  string += "(" + year + "). " + formatTitle
  htmlCitation += "(" + year + "). " + formatTitle
  if(title.last() != '.' && title.last() != '!' && title.last() != '?'){
      string += '.'
      htmlCitation += '.'
  } else{
      string += ''
    }

  // Adding jounal title, volume, and range of pages
  if(typeof journal !== 'undefined' && journal != ""){
      string += ' ' + journal + ', '
      htmlCitation += ' ' + "<i>" + journal + "</i>" + ', '
    }

  if(typeof volume !== 'undefined' && volume){
      string += volume + ', '
      htmlCitation += "<i>" + volume + "</i>" + ', '
    }

  if(typeof page !== 'undefined' && page){
      string += page + "."
      htmlCitation += page + "."
    }

  if(typeof doi !== 'undefined' && doi && type != 'book-chapter' && type != 'book'){
      string += " doi\:" + doi
      htmlCitation += " doi\:" + doi
    }
}
htmlCitation += "</p>"

  var citationForm = $('#id_author-0-citation');
  citationForm.val(string)
alert("Citation Meta-Data Retrieved Succesfully!");
modal.style.display = "none";
})


});

});
