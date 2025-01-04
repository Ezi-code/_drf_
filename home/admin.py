"""Admin models for home app."""

from django.contrib import admin
from home.models import Person, Color


class AdminPerson(admin.ModelAdmin):
    """Admin model for Person."""

    list_display = ["name", "age", "color"]
    search_fields = ["name", "age", "color"]
    list_filter = ["name", "age", "color"]


admin.site.register(Person, AdminPerson)


class AdminColor(admin.ModelAdmin):
    """Admin model for Color."""

    list_display = ["color_name"]
    search_fields = ["color_name"]
    list_filter = ["color_name"]


admin.site.register(Color, AdminColor)
