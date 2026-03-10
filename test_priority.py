import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client
from todos.models import Todo
from django.contrib.auth.models import User
import json

client = Client()

# Login
client.post('/login/', {'username': 'admin', 'password': 'admin123'})

# Create two tasks
user = User.objects.get(username='admin')
t1 = Todo.objects.create(text='Task 1', owner=user)
t2 = Todo.objects.create(text='Task 2', owner=user)

# Call API to update priorities
payload = [
    {'id': t2.id, 'priority': 0, 'status': 'OPEN'},
    {'id': t1.id, 'priority': 1, 'status': 'ONGOING'},
]

response = client.post('/todos/api/update_priority/', json.dumps(payload), content_type='application/json')
print('API Response:', response.status_code, response.content)

# Verify in DB
t1.refresh_from_db()
t2.refresh_from_db()
print('T1 Priority:', t1.priority, 'Status:', t1.status)
print('T2 Priority:', t2.priority, 'Status:', t2.status)
