import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from todos.models import Todo

User = get_user_model()
django.conf.settings.ALLOWED_HOSTS = ['testserver']
c = Client()

def test_frontend():
    print("=== Testing Frontend Functionality ===")
    
    # Setup users
    writer, _ = User.objects.get_or_create(username='frontend_writer')
    writer.set_password('pass123')
    writer.is_staff = False
    writer_group, _ = Group.objects.get_or_create(name='Writer')
    writer.groups.add(writer_group)
    writer.save()

    # Login
    assert c.login(username='frontend_writer', password='pass123'), "Login failed"

    # Step 1: Create a Todo using the frontend POST
    resp = c.post('/todos/create/', {'text': 'ASVS Test Todo'})
    # It should redirect to /todos/ or /
    if resp.status_code == 302 and resp.url in ['/todos/', '/']:
        print("[PASS] Writer can create a todo")
    else:
        print(f"[FAIL] Writer creation logic failed. Status: {resp.status_code}, URL: {getattr(resp, 'url', 'N/A')}")
        return

    # Check DB
    todo = Todo.objects.filter(text='ASVS Test Todo').first()
    if not todo:
        print("[FAIL] Todo was not saved to DB")
        return
    print(f"[PASS] Todo created successfully with ID {todo.id}")

    # Step 2: Try to update the status via frontend POST
    # We navigate to /todos/<id>/update/ instead of /admin/todos/...
    resp = c.post(f'/todos/{todo.id}/update/', {'status': 'CLOSED'})
    if resp.status_code == 302 and resp.url in ['/todos/', '/']:
        print("[PASS] Writer can submit status change on the frontend")
    else:
        print(f"[FAIL] Writer update logic failed. Status: {resp.status_code}")
        if resp.status_code == 500:
            print("[FAIL] Encountered 500 internal server error. Probably TemplateSyntaxError.")
        return

    # Verify update
    todo.refresh_from_db()
    if todo.status == 'CLOSED':
        print("[PASS] Todo status updated correctly in DB")
    else:
        print(f"[FAIL] Status is not CLOSED. Status is {todo.status}")
        return

    print("=== All Frontend Tests Passed! ===")

if __name__ == '__main__':
    test_frontend()
