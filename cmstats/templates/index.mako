<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>CMStats</title>
        <link rel="stylesheet" type="text/css" href="/static/css/core.css" />
    </head>
    <body>
        <h3>Total Installs</h3>
        <table>
            <tr>
                <th width="250">Type</th>
                <th>Total</th>
            </tr>
            <tr>
                <td>Official Installs</td>
                <td>${total_nonkang}</td>
            </tr>
            <tr>
                <td>Unofficial Installs (KANGs)</td>
                <td>${total_kang}</td>
            </tr>
            <tr>
                <td><b>TOTAL</b></td>
                <td><b>${total_kang + total_nonkang}</b></td>
            </tr>
        </table>
        
        <h3>Installs by Version</h3>
        <table>
            <tr>
                <th width="250">Version</th>
                <th>Total</th>
            </tr>
            % for version in version_count:
            <tr><td>${version[1]}</td><td>${version[0]}</td></tr>
            % endfor
        </table>
        
        <h3>Installs by Device</h3>
        <table>
            <tr>
                <th width="250">Device</th>
                <th>Total</th>
            </tr>
            % for device in device_count:
            <tr><td>${device[1]}</td><td>${device[0]}</td></tr>
            % endfor
        </table>
    </body>
</html>