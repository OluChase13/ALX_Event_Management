from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # Replace your_project_name

wsgi_app = get_wsgi_application()

def application(environ, start_response):
    # Set the script name to ensure Django URLs work correctly
    environ['SCRIPT_NAME'] = '/api'
    return wsgi_app(environ, start_response)