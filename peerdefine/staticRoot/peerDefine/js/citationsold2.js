var interpretation = {}
var evalRaw = {}
Array.prototype.last = function(){
        return this[this.length - 1];
    };
String.prototype.last = function(){
  return this[this.length - 1];
}

var num = 0;
var flag = false;
var searchedValue = $('#citationInput').val();
$('#citationSubmit').click(function(event) {
  var searchedValue = $('#citationInput').val();
  if ($('#searchType').val() == 'title') {
  var params = {
    // Request parameters
    "query": searchedValue,
    "complete": "0",
    "count": "10",
    "model": "latest",
  };
  $.ajaxSetup({
    headers: {
      'Ocp-Apim-Subscription-Key': '72e27eb68b684a04b60e7fa0ecc5efc6'
    }
  });

  // var interpretation = JSON.parse(raw['responseText'])['interpretations'][0]['rules'][0]['output']['value'];

  var raw = $.getJSON("https://api.labs.cognitive.microsoft.com/academic/v1.0/interpret?" +
    $.param(params),
    function(json) {
      if (typeof raw !== 'undefined' && typeof raw['responseText'] !== 'undefined') {
      interpretation =
        JSON.parse(raw['responseText'])['interpretations'][0]['rules']
        [0]['output']['value'];

      var paramsEval = {
        // Request parameters
        "expr": interpretation,
        "model": "latest",
        "count": "10",
        "offset": "0",
        "attributes": 'Ti,Y,CC,AA.AuN,AA.DAuN,AA.AuId,E.VFN,E.DN,J.JId,E.DOI,E.V,E.I,E.FP,E.LP,AA.S,E'
      };
      evalRaw = $.getJSON("https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?" + $.param(paramsEval), function(json) {
        evalClean = JSON.parse(evalRaw['responseText'])['entities'][0]
        authors = evalClean['AA']
        title = evalClean['DN']
        year = evalClean['Y']
        journal = evalClean['VFN']
        volume = evalClean['V']
        issue = evalClean['I']
        firstPage = evalClean['FP']
        lastPage = evalClean['LP']
        citations = evalClean['CC']
        doi = JSON.parse(evalClean['E'])['DOI']

        var yearForm = $('#id_year');
        yearForm.val(year)


        authorsLen = authors.length;
        authorList = []
        for (var i = 0; i < authorsLen; i++) {
          authorList.push(authors[i]['DAuN'])
        };


                  var yearForm = $('#id_year');
                  yearForm.val(year)

                  authorsLen = authors.length;
                  authorList = []
                  for (var i = 0; i < authorsLen; i++) {
                    authorList.push(authors[i]['DAuN'])
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
        string += "(" + year + "). " + formatTitle
        if(title.last() != '.'){
            string += '.'
        } else{
            string += ''
          }

        // Adding jounal title, volume, and range of pages
        if(journal != ""){
            string += ' ' + journal + ', '
          }

        if(volume){
            string += volume + ', '
          }

        if(firstPage){
            string += firstPage + '-'
          }

        if(lastPage){
            string += lastPage + "."
          }

        if(doi){
            string += " doi\:" + doi
          }
          var citationForm = $('#id_author-0-citation');
          citationForm.val(string)
        alert("Citation Meta-Data Retrieved Succesfully!");
        modal.style.display = "none";

      })


    }else if(typeof raw['responseText']['interpretations'] === 'undefined' && num < 1){
      flag = true;
      delete $.ajaxSettings.headers["Ocp-Apim-Subscription-Key"];
      $('#citationSubmit').click()
      num += 1
    }
  });
}

if (flag == true || $('#searchType').val() == 'doi'){
  var searchedValue = $('#citationInput').val();
  if(typeof $.ajaxSettings.headers !== 'undefined' &&
  typeof $.ajaxSettings.headers["Ocp-Apim-Subscription-Key"] !== 'undefined'){
    delete $.ajaxSettings.headers["Ocp-Apim-Subscription-Key"];
  }
  crossSite = ''
  rows = ''
  if(searchedValue.search('/') != -1){
    crossSite = 'https://api.crossref.org/v1/works/'
    searchedValue = searchedValue.trim()
    rows = ''
  }else {
    crossSite = 'https://api.crossref.org/works?query='
    rows = "&rows=1"
  }
  evalTest = $.getJSON(crossSite + searchedValue + rows,
function(json) {
  if(rows == "&rows=1"){
  evalClean = JSON.parse(evalTest['responseText'])['message']['items'][0]
} else {evalClean = JSON.parse(evalTest['responseText'])['message']
}
  authors = evalClean['author']
  title = evalClean['title']
  containerTitle = evalClean['container-title']
  year = ''
  if(evalClean['published-online'])
  { year = evalClean['published-online']['date-parts'][0][0]
} else if(evalClean['published-print']){
  year = evalClean['published-print']['date-parts'][0][0]
}

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
            for(var i = 1; i<authorList.length-1; i++){
            inTextList += authorList[i].split(" ").last().concat(", ") }
            inTextList += "& " + authorList[authorList.length-1].split(" ").last().concat(", ")
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
});
}
});
