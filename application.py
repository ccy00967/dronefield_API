from core.wsgi import application as django_application

def application(environ, start_response):
    try:
        # 요청 본문 크기를 안전하게 처리
        request_body_size = int(environ.get('CONTENT_LENGTH', 0) or 0)
        request_body = environ['wsgi.input'].read(request_body_size)

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"Request processed successfully"]

    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [str(e).encode()]

# Django 애플리케이션이 기본 WSGI 애플리케이션으로 작동하도록 설정
application = django_application
