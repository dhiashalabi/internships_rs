from django.contrib import admin
from .models import UserProfile, UserProfileItem


class UserProfileItemInline(admin.TabularInline):
    model = UserProfileItem
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserProfileItemInline]
