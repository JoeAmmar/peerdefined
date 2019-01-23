var interpretation = {}
var evalRaw = {}
Array.prototype.last = function(){
        return this[this.length - 1];
    };
String.prototype.last = function(){
  return this[this.length - 1];
}
$('#citationSubmitBook').click(function(event) {
  var googleSearch = $('#citationInputBook').val();
      var rawBooks = {
        // Request parameters
        "q": googleSearch,
        "key": "AIzaSyClZzTlTlk_6yBtuC2cVG_n-Ess3xRepwc"
            };
        evalRawBook = $.getJSON("https://www.googleapis.com/books/v1/volumes?" + $.param(rawBooks), function(json) {

        evalClean = JSON.parse(evalRawBook['responseText'])['items'][0]['volumeInfo']
        authors = evalClean['authors']
        title = evalClean['title']
        year = evalClean['publishedDate'].substring(0,4)
        publisher = evalClean['publisher']
        pages = evalClean['pageCount']
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
                titleChars[titleIndex + 1] = titleChars[titleIndex + 1].upper()
            } else if(titleChars[titleIndex + 2] != ' '){
                titleChars[titleIndex + 2] = titleChars[titleIndex + 2].upper()}};
        formatTitle = titleChars.join("")




        // Adding title information to citation
        string += "(" + year + "). " + formatTitle
        if(title[-1] != '.'){
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


    });

});
