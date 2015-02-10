<!doctype html>
<html>

<head>
  <title>All episodes</title>
  <link rel="stylesheet" href="/css/main.css">
</head>

<body>

  <div class="header">
    <nav><strong>How I met your mother graph</strong></nav>
  </div>

  <h1>How I met your mother graph</h1>

  <ul>
    % for id, title in episodes:
    <li><a href="/episodes/{{id}}">{{title}}</a></li>
    % end
  </ul>

  <div class="footer">
    <code>(graphs)-[:ARE]->(everywhere)</code>
    <p>With &hearts; from Sweden &amp; the <a href="http://neo4j.com/community/">Neo4j Community</a></p>
  </div>

</body>

</html>
