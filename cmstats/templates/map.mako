<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>CMStats</title>
        <link rel="stylesheet" type="text/css" href="/static/css/core.css" />
        <script type="text/javascript" src="http://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load('visualization', '1', {'packages':['geomap', 'table']});
            google.setOnLoadCallback(function(){
                drawChart();
            });
            
            function drawChart() {
                drawCountryChart();
            }

            function drawCountryChart() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Country');
                data.addColumn('number', 'Installs');
                data.addColumn('string', 'hover');
                data.addRows([
                    % for value in country_data:
                    ['${value[0]|h}', ${value[1]|h}, '${value[0]|h}'],
                    % endfor
                ]);
                var chart = new google.visualization.GeoMap(document.getElementById('map'));
                chart.draw(data, {width:681, height: 440});
            }
        </script>
    </head>
    <body>
        
        <div style="text-align: center">
            <h2>Installations by Country</h2>
            <div id="map"></div>
        </div>

    </body>
</html>
