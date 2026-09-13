from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, StatusUpdate


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional information', {
            'fields': ('role', 'bio', 'profile_picture'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional information', {
            'fields': ('role', 'bio', 'profile_picture'),
        }),
    )

@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')