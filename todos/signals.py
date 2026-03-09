from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import AuthLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuthLog.objects.create(
        username=user.username,
        successful=True,
        details="User logged in successfully."
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    username = credentials.get('username', 'Unknown')
    AuthLog.objects.create(
        username=username,
        successful=False,
        details="Login failed with provided credentials."
    )

def on_saml_user_create(user_identity):
    """
    Triggered after a new user is created by PySAML2.
    It provisions the user with `is_staff = True` so they can access the Django admin,
    but assigns them to the "Reader" group to limit their access to read-only views.
    """
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    User = get_user_model()
    
    # We find the user by their email, mapped from NameID
    user = User.objects.filter(email=user_identity.get('name', [None])[0]).first()
    if user:
        # Assign to Reader group
        try:
            reader_group = Group.objects.get(name='Reader')
            user.groups.add(reader_group)
        except Group.DoesNotExist:
            pass
