"""Exercise the actual ZIP in an isolated directory, without DB or cloud access."""
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CHECK = r'''
import os, unittest
from pathlib import Path
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_azure'
import django
django.setup()
from django.conf import settings
from django.test import Client, RequestFactory
from config.wsgi_azure import application

class ProductionPackageTests(unittest.TestCase):
    def test_https_and_host(self):
        c = Client(HTTP_HOST='ecogest-test.azurewebsites.net')
        self.assertEqual(c.get('/').status_code, 301)
        self.assertEqual(Client(HTTP_HOST='untrusted.example').get('/', secure=True).status_code, 400)
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertEqual(settings.DATABASES['default']['OPTIONS']['sslmode'], 'require')
        self.assertEqual(settings.MEDIA_ROOT.as_posix(), '/home/ecogest/media')
        self.assertFalse(settings.AI_ENABLED)

    def test_spa_routes_and_private_paths(self):
        c = Client(HTTP_HOST='ecogest-test.azurewebsites.net')
        for route in ['/', '/registros', '/planes', '/asistente', '/lotes/1234-abcd']:
            response = c.get(route, secure=True)
            self.assertEqual(response.status_code, 200, route)
            self.assertIn(b'<div id="root">', b''.join(response.streaming_content))
            self.assertEqual(response['Cache-Control'], 'no-cache')
        for route in ['/media/private.pdf', '/.env', '/config/settings.py', '/unknown']:
            self.assertEqual(c.get(route, secure=True).status_code, 404, route)

    def test_api_auth_and_csrf(self):
        c = Client(enforce_csrf_checks=True, HTTP_HOST='ecogest-test.azurewebsites.net')
        self.assertEqual(c.get('/api/session/csrf', secure=True).status_code, 200)
        self.assertIn(c.get('/api/lots', secure=True).status_code, [401, 403])
        self.assertEqual(c.post('/api/session/login', {}, secure=True).status_code, 403)

    def test_static_assets(self):
        for path in Path('web/assets').iterdir():
            statuses = []
            request = RequestFactory().get('/assets/' + path.name, secure=True,
                                           HTTP_HOST='ecogest-test.azurewebsites.net')
            body = application(request.environ, lambda status, headers: statuses.append(status))
            try:
                self.assertEqual(b''.join(body), path.read_bytes())
            finally:
                if hasattr(body, 'close'): body.close()
            self.assertTrue(statuses[0].startswith('200'))

unittest.main()
'''

with zipfile.ZipFile(ROOT / "build/azure/ecogest.zip") as archive:
    for name in archive.namelist():
        parts = Path(name).parts
        assert not Path(name).is_absolute() and ".." not in parts
        assert not any(part in {".env", ".venv", "media", "node_modules", ".git"} for part in parts)
        assert Path(name).suffix not in {".pem", ".key", ".dump", ".backup", ".map"}
    with tempfile.TemporaryDirectory(prefix="ecogest-azure-check-") as directory:
        archive.extractall(directory)
        environment = dict(os.environ, DJANGO_SECRET_KEY="test-only-" + "a" * 60,
                           DB_PASSWORD="unused-local-test", AZURE_APP_HOST="ecogest-test.azurewebsites.net")
        subprocess.run([str(ROOT / "backend/.venv/Scripts/python.exe"), "-c", CHECK],
                       cwd=directory, env=environment, check=True)
print("ZIP verificado sin secretos locales ni conexiones a Azure/PostgreSQL.")
