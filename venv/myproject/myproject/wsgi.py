"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the Python path
project_path = 'C:\\Users\\pc\\OneDrive\\Desktop\\AUTH_SYSTEM\\venv\\myproject\\myproject'
if os.path.exists(project_path) and os.path.isfile(os.path.join(project_path, '__init__.py')):
    sys.path.insert(0, project_path)
else:
    print(f"Project path: {project_path} does not exist or is not a valid Python package.")



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
app = application
