<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
  <title>SwiftMend</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f0f0f0;
    }
    h2 {
      color: #333;
      text-align: center;
      margin-top: 50px;
    }
    #data {
      width: 80%;
      margin: 50px auto;
      padding: 20px;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    button {
      display: block;
      width: 200px;
      height: 40px;
      margin: 20px auto;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    button:hover {
      background-color: #45a049;
    }
    /* Table styles */
    table {
      width: auto;
      border-collapse: collapse;
    }
    th, td {
      padding: 10px;
      text-align: center;
      border: 1px solid #ddd;
    }
    th {
      background-color: #4CAF50;
      color: white;
    }
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    tr:hover {
      background-color: #ddd;
    }
  </style>
  <script>
    function refreshData() {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var display = document.getElementById("data");
          var path = document.getElementById("path").value;
          if (path == '/footprint') {
            var footprintMatrix = JSON.parse(xhr.responseText);
            var table = '<table border="1">';
            // Add header row
            table += '<tr><th></th>'; // Empty cell at the beginning
            for (var i = 0; i < footprintMatrix.length; i++) {
              table += '<th>' + i + '</th>';
            }
            table += '</tr>';
            for (var i = 0; i < footprintMatrix.length; i++) {
              table += '<tr>';
              // Add left side column
              table += '<th>' + i + '</th>';
              for (var j = 0; j < footprintMatrix[i].length; j++) {
                table += '<td>' + footprintMatrix[i][j] + '</td>';
              }
              // // Add right side column
              // table += '<th>' + i + '</th>';
              // table += '</tr>';
            }
            table += '</table>';
            display.innerHTML = table;

            // Send another GET request to get the index list
            var xhr2 = new XMLHttpRequest();
            xhr2.onreadystatechange = function() {
              if (xhr2.readyState == 4 && xhr2.status == 200) {
                display.innerHTML += '<br>' + xhr2.responseText;
              }
            };
            xhr2.open("GET", "/distinctActivities", true);
            xhr2.send();
          } else if (path == '/directlyFollows'){
            var directlyFollowsMatrix = JSON.parse(xhr.responseText);
            var table = '<table border="1">';
            // Add header row
            table += '<tr><th></th>'; // Empty cell at the beginning
            for (var i = 0; i < directlyFollowsMatrix.length; i++) {
              table += '<th>' + i + '</th>';
            }
            table += '</tr>';
            for (var i = 0; i < directlyFollowsMatrix.length; i++) {
              table += '<tr>';
              // Add left side column
              table += '<th>' + i + '</th>';
              for (var j = 0; j < directlyFollowsMatrix[i].length; j++) {
                table += '<td>' + directlyFollowsMatrix[i][j] + '</td>';
              }
              table += '</tr>';
            }
            table += '</table>';
            display.innerHTML = table;
          } else {
            display.innerHTML = xhr.responseText;
          }
        }
      };
      var path = document.getElementById("path").value;
      xhr.open("GET", path, true);
      xhr.send();
    }
    setInterval(refreshData, 2000); // Refresh every 2 seconds
  </script>
</head>
<body>
<h2>SwiftMend</h2>
<input type="hidden" id="path" value="/cases">
<button onclick="document.getElementById('path').value='/cases';refreshData();">Cases</button>
<button onclick="document.getElementById('path').value='/distinctActivities';refreshData();">Distinct Activities</button>
<button onclick="document.getElementById('path').value='/footprint';refreshData();">Footprint</button>
<button onclick="document.getElementById('path').value='/directlyFollows';refreshData();">Directly Follows</button>
<button onclick="document.getElementById('path').value='/clusters';refreshData();">Merge Set</button>
<div id="data">Loading...</div>
</body>
</html>