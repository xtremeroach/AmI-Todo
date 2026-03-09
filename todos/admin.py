from django.contrib import admin
from .models import Todo, AuthLog

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'status')
    list_filter = ('status',)

@admin.register(AuthLog)
class AuthLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'username', 'successful')
    list_filter = ('successful', 'timestamp')
    search_fields = ('username', 'details')

    # Make AuthLog read-only for debug purposes
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
