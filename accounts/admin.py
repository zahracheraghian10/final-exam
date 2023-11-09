from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from accounts.models import Users


@admin.register(Users)
class UserAdmin(DefaultUserAdmin):
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_display = ('username', 'phone', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_editable = ('is_staff', 'is_active')