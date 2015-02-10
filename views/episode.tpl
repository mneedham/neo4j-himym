<!doctype html>
<html>

<head>
  <title>Episode {{episode['id']}}</title>
  <link rel="stylesheet" href="/css/main.css">
</head>

<body>

  <div class="header">
    <nav><strong>{{episode['title']}}</strong></nav>
  </div>

  <div>
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


</body>

</html>
