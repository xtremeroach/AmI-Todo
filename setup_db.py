import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User, Group

def setup():
    # Create Groups
    reader_group, _ = Group.objects.get_or_create(name='reader')
    writer_group, _ = Group.objects.get_or_create(name='writer')
    admin_group, _ = Group.objects.get_or_create(name='admin')

    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', os.getenv('DJANGO_SUPERUSER_PASSWORD'))
        print("Superuser 'admin' created.")
    else:
        admin_user = User.objects.get(username='admin')
        print("Superuser 'admin' already exists.")

    # Assign superuser to admin group
    admin_user.groups.add(admin_group)
    print("Initial setup complete.")

if __name__ == '__main__':
    setup()
