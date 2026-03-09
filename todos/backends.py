from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = username or kwargs.get('email')
        if email:
            # Look up the user by email address
            user = UserModel.objects.filter(email__iexact=email).first()
            if user and user.check_password(password):
                return user
        return None
