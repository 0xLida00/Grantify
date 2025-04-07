from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MyModel

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('username', 'email', 'role')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# Register MyModel
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')