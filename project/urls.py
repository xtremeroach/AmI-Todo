"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import django.conf.urls
import django.utils.http
from django.utils.http import url_has_allowed_host_and_scheme

# Monkeypatches for django-saml2-auth < 3.0
django.conf.urls.url = re_path
django.utils.http.is_safe_url = url_has_allowed_host_and_scheme

import django_saml2_auth.views
from todos.views import local_login

# Restrict generic admin access to 'admin' group or superusers
original_has_permission = admin.site.has_permission

def custom_admin_has_permission(request):
    is_active = request.user.is_active
    is_admin_role = request.user.is_superuser or request.user.groups.filter(name='admin').exists()
    return is_active and is_admin_role

admin.site.has_permission = custom_admin_has_permission

urlpatterns = [
    path('admin/login/', django_saml2_auth.views.signin),  # Force SSO Login
    path('admin/logout/', django_saml2_auth.views.signout), # Force SSO Logout
    path('admin/', admin.site.urls),
    path('login/', local_login, name='login'),
    path('saml2_auth/signin/', django_saml2_auth.views.signin),
    path('saml2_auth/signout/', django_saml2_auth.views.signout),
    path('saml2_auth/', include('django_saml2_auth.urls')),
    path('todos/', include('todos.urls')),
    path('', include('todos.urls')), # Redirect root to todos
]
