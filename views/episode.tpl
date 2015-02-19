<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Season {{episode['season']}}, Episode{{episode['number']}}: {{episode['title']}}</title>

  <!-- Bootstrap Core CSS -->
  <link href="/css/bootstrap.css" rel="stylesheet">

  <!-- Custom CSS -->
  <style>
  body {
    padding-top: 70px;
    /* Required padding for .navbar-fixed-top. Remove if using .navbar-static-top. Change if height of navigation changes. */
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
    <h1>{{episode['title']}}</h1>

    <!-- Nav tabs -->
    <ul class="nav nav-tabs" role="tablist">
      <li role="presentation" class="active"><a href="#overview" aria-controls="overview" role="tab" data-toggle="tab">Overview</a></li>
      <li role="presentation"><a href="#topics" aria-controls="topics" role="tab" data-toggle="tab">Topics</a></li>
      <li role="presentation"><a href="#transcript" aria-controls="transcript" role="tab" data-toggle="tab">Transcript</a></li>
    </ul>

    <!-- Tab panes -->
    <div class="tab-content">
      <div role="tabpanel" class="tab-pane active" id="overview">

      </div>
      <div role="tabpanel" class="tab-pane" id="topics">
        <table class="table">
          <tr>
            <th align="left">Topic</th>
            <th align="left">Score</th>
          </tr>
          % for topic in episode['topics']:
          <tr>
            <td><a href="/topics/{{topic['id']}}">{{topic['name']}}</a></td>
            <td>{{topic['score']}}</td>
          </tr>
          %end
        </table>
      </div>
      <div role="tabpanel" class="tab-pane" id="transcript">
        <table class="table">
          % for sentence in sentences:
          <tr>
            <td>{{sentence}}</td>
          </tr>
          %end
        </table>
      </div>
    </div>
  </div>
  <!-- /.container -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
  <script src="/js/bootstrap.js"></script>
</body>
</html>
