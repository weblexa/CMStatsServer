<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>CMStats</title>
        <link rel="stylesheet" type="text/css" href="/static/css/core.css" />
    </head>
    <body>
    <table>
    <tr>
        <th>Device</th>
        <th>Total</th>
    </tr>
    % for device in device_count:
    <tr><td>${device[1]}</td><td>${device[0]}</td></tr>
    % endfor
    <tr><td><b>Total</b></td><td><b>${total_devices}</b></td></tr>
    </table>
    </body>
</html>