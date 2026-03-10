from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('api/users/search/', views.user_search, name='user_search'),
]
