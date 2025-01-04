from core.wsgi import application

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"Request processed successfully"]
        
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [str(e).encode()]
