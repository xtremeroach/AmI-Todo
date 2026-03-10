import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client

client = Client()

print("--- Testing Normal User ---")
response = client.post('/login/', {'username': 'normaluser', 'password': 'normal123'})
print('Normal user login redirect:', response.url if response.status_code == 302 else response.status_code)
response = client.get('/admin/')
print('Normal user /admin/ status:', response.status_code)

print("\n--- Testing Superuser Admin ---")
client.logout()
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
response = client.get('/admin/')
print('Admin user /admin/ status:', response.status_code)

print("\n--- Testing Group Admin ---")
client.logout()
client.post('/login/', {'username': 'groupadmin', 'password': 'group123'})
response = client.get('/admin/')
print('Group Admin /admin/ status:', response.status_code)
