import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from todos.models import Todo

User = get_user_model()
django.conf.settings.ALLOWED_HOSTS = ['testserver']
c = Client()

def run_tests():
    # Setup Users
    reader, _ = User.objects.get_or_create(username='reader', email='reader@test.com')
    reader.set_password('pass')
    reader.is_staff = True
    reader_group = Group.objects.get(name='Reader')
    reader.groups.add(reader_group)
    reader.save()

    writer, _ = User.objects.get_or_create(username='writer', email='writer@test.com')
    writer.set_password('pass')
    writer.is_staff = True
    writer_group = Group.objects.get(name='Writer')
    writer.groups.add(writer_group)
    writer.save()

    print("--- Testing Reader ---")
    assert c.login(username='reader', password='pass'), "Reader login failed"

    # Reader tries to view todos (should succeed)
    resp = c.get('/admin/todos/todo/')
    if resp.status_code == 200:
        print("[PASS] Reader can view todos list")
    else:
        print(f"[FAIL] Reader view failed: {resp.status_code}")

    # Reader tries to create a todo (should fail)
    resp = c.post('/admin/todos/todo/add/', {'text': 'Reader Todo', 'status': 'OPEN'})
    if resp.status_code == 403:
        print("[PASS] Reader is forbidden from creating todo")
    else:
        print(f"[FAIL] Reader creation unexpected status: {resp.status_code}")

    # Reader tries to view users (should have read-only or no access)
    resp = c.get('/admin/auth/user/')
    if resp.status_code in [200, 403]: 
        print(f"[PASS] Reader viewing users status: {resp.status_code} (Expected 200/403)")
    else:
        print(f"[FAIL] Reader viewing users unexpected status: {resp.status_code}")
        
    # Reader tries to change settings (users)
    if User.objects.exists():
        first_user_id = User.objects.first().id
        resp = c.post(f'/admin/auth/user/{first_user_id}/change/', {'username': 'hacked'})
        if resp.status_code == 403:
            print("[PASS] Reader is forbidden from changing users/settings")
        else:
            print(f"[FAIL] Reader change users expected 403, got: {resp.status_code}")

    c.logout()

    print("--- Testing Writer ---")
    assert c.login(username='writer', password='pass'), "Writer login failed"

    # Writer tries to create a todo (should succeed)
    resp = c.post('/admin/todos/todo/add/', {'text': 'Writer Todo', 'status': 'OPEN'})
    if resp.status_code == 302:
        print("[PASS] Writer successfully created a todo")
    else:
        print(f"[FAIL] Writer creation unexpected status: {resp.status_code}")

    # Check if todo was created
    todo = Todo.objects.filter(text='Writer Todo').first()
    if todo:
        print("[PASS] Writer Todo actually exists in DB")
        
        # Writer tries to change status
        resp = c.post(f'/admin/todos/todo/{todo.id}/change/', {'text': 'Writer Todo', 'status': 'CLOSED'})
        if resp.status_code == 302:
            print("[PASS] Writer successfully submitted change todo status")
            todo.refresh_from_db()
            if todo.status == 'CLOSED':
                print("[PASS] Writer Todo status is actually CLOSED in DB")
            else:
                print(f"[FAIL] Writer Todo status didn't update in DB: {todo.status}")
        else:
            print(f"[FAIL] Writer update unexpected status: {resp.status_code}")
    else:
        print("[FAIL] Writer Todo missing from DB")

    c.logout()

if __name__ == '__main__':
    run_tests()
