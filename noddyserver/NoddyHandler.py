from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

page = '''\
<html>
<head>
<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate'/>
<meta http-equiv='Pragma' content='no-cache'/>
<meta http-equiv='Expires' content='0'/>
</head>
<body>
<h1>DaSync</h1>
<h2>Results</h2>
{results}
<h2>Errors</h2>
{errors}
<hr>
<form action='/insert'>
<input type='text' name='license' size='32' maxlength='32' value='{license}'/><br>
<input type='submit'/>
</form>

<form action='/reset'>
<input type='submit' value='Reset Table' />
</form>

<form action='/list'>
<input type='submit' value='List Table' />
</form>

</body>
</html>
'''

class NoddyHandler(BaseHTTPRequestHandler):
    def __init__(self, db, license, *args, **kwargs):
        self.db = db
        self.license = license
        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)

    def response(self, request):
        # Parse request
        parsed_url = urlparse(request)
        request_type = parsed_url.path.lstrip('/').lower()
        params = parse_qs(parsed_url.query)
    
        # Handle request
        errors = []
        results = []
        if request_type == 'insert':
            if 'license' in params:
                try:
                    newLicense = parse_qs(parsed_url.query)['license'][0]
                    results.extend(['insert', newLicense])
                    res, err = self.db.insert(newLicense)
                    results.extend(res)
                    errors.extend(err)
                except Exception as e:
                    errors.append(str(e))
        elif request_type == 'list':
            results.append("list")
            res, err = self.db.list()
            results.extend(res)
            errors.extend(err)
        elif request_type == 'reset':
            results.append("reset")
            res, err = self.db.recreate()
            results.extend(res)
            errors.extend(err)
    
        # Compute status
        status = 500
        if len(errors) > 0:
            status = 400
        elif len(results) > 0:
            status = 200
    
        return status, results, errors

    def do_GET(self):
        result, results, errors = self.response(self.path)
        self.send_response(result)
        self.end_headers()
        self.wfile.write(bytes(page.format(results='<br>'.join(results), errors='<br>'.join(errors), license=self.license), encoding='utf-8'))
