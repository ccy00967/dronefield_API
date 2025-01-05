import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 애플리케이션 객체 노출
application = get_wsgi_application()
