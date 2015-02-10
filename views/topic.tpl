<!doctype html>
<html>

<head>
  <title>Topic {{topic['id']}}</title>
  <link rel="stylesheet" href="/css/main.css">
</head>

<body>

  <div class="header">
    <nav><strong>{{topic['value']}}</strong></nav>
  </div>

  <div>
    <table class="table">
      <tr>
        <th align="left">Topic</th>
        <th align="left">Score</th>
      </tr>
      % for episode in topic['episodes']:
      <tr>
        <td><a href="/episodes/{{episode['id']}}">{{episode['title']}}</a></td>
        <td>{{episode['score']}}</td>
      </tr>
      %end

    </table>

  </div>


</body>

</html>
