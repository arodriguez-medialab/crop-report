from django.contrib import admin
from user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ('username', 'first_name', 'last_name','is_staff', 'is_active')
    fieldsets = (
    ("Datos personales", {'fields': ('username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff')}),
    ('Permisos', {'fields': ('groups', 'user_permissions',)}),
)