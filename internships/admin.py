from django.contrib import admin
from .models import (
    User,
    Country,
    City,
    InternshipCategory,
    InternshipType,
    Internship,
    UserInterest,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "gender",
        "is_active",
        "is_superuser",
    )
    search_fields = (
        "name",
        "username",
        "first_name",
    )
    fieldsets = [
        (
            None,
            {
                "fields": ("password", "is_active", "is_staff", "is_superuser"),
            },
        ),
        (
            None,
            {
                "fields": (
                    ("last_login", "date_joined"),
                    # ("groups", "user_permissions"),
                    ("username", "first_name", "last_name"),
                    ("country", "city", "location"),
                    ("email", "phone", "gender"),
                    ("profile",),
                )
            },
        ),
    ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country")
    search_fields = ("name", "country")
    fieldsets = [
        (
            None,
            {"fields": (("name", "state", "country"),)},
        ),
    ]


@admin.register(InternshipCategory)
class InternshipCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(InternshipType)
class InternshipTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "start_date", "end_date")
    search_fields = ("title", "company", "location")
    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("title", "internship_category", "internship_type"),
                    "description",
                    ("image", "company", "location"),
                    ("country", "city"),
                    ("start_date", "end_date", "apply_by"),
                    ("duration", "stipend", "url"),
                )
            },
        ),
    ]


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    autocomplete_fields = ("internships",)
    list_display = ("user", "full_name")

    def full_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
