import os
from django.core.wsgi import get_wsgi_application
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

logger = logging.getLogger(__name__)

def application_with_content_length_handling(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (KeyError, ValueError):
        request_body_size = 0
    
    logger.info(f"Request body size: {request_body_size}")
    
    # 기본 WSGI 애플리케이션 호출
    return application(environ, start_response)