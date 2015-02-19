<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Training speakers: How I met your mother graph</title>

  <!-- Bootstrap Core CSS -->
  <link href="/css/bootstrap.css" rel="stylesheet">

  <!-- Custom CSS -->
  <style>
  body {
    padding-top: 70px;
    /* Required padding for .navbar-fixed-top. Remove if using .navbar-static-top. Change if height of navigation changes. */
  }

  span.training {
    border: 1px black solid;
    padding: 5px;
    display: inline-block;
    margin: 2px
  }

  span.training:hover {
    cursor: pointer; cursor: hand;
  }

  span.speaker {
    background-color: yellow;
  }
  </style>

  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
  <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
  <![endif]-->

</head>

<body>

  % include('nav.tpl')

  <!-- Page Content -->
  <div class="container">
    <h1>Training speakers</h1>
    <div class="bs-example">
      <form class="sentences">
        <table class="table">

        </table>
        <input type="submit" value="Train Data" class="btn btn-default">
      </form>
    </div>

  </div>
  <!-- /.container -->

  <script type="text/javascript" src="js/jquery-2.1.3.js"></script>

  <script type="text/javascript">
    var loadSentences = function() {
      $.getJSON( "/training", function( json ) {
        $.each(json.sentences, function() {
          var row = $(this);

          var htmlRow = "<tr><td class='sentenceToTrain'>";
          $.each(row, function() {
            htmlRow += "<span class='training'>" + this + "</span>";
          })
          htmlRow += "</td></tr>"

          $("table.table").append(htmlRow)
        })

        $("span.training").on('click', function(event) {
          if($(this).hasClass("speaker")) {
            $(this).removeClass("speaker");
          } else {
            $(this).addClass("speaker");
          }
        });
      });
    };

    var clearSentences = function() {
      $("table.table tr").remove()
    }

    loadSentences();

    $("form.sentences").submit(function( event ) {
      var sentences = [];

      $("td.sentenceToTrain").each(function() {
        var item = $(this);

        var words = [];
        item.find("span.training").each(function() {
          words.push({word: $(this).text(), speaker: $(this).hasClass("speaker")})
        });

        sentences.push({words: words})
      });
      console.log(sentences)

      $.ajax("/training", {
        data : JSON.stringify(sentences),
        contentType : 'application/json',
        type : 'POST'
      }).done(function() {
        console.log("success");
        clearSentences();
        loadSentences();
      });
      event.preventDefault();
    });
  </script>
</body>
</html>
