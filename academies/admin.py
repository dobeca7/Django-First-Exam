from django.contrib import admin

from academies.models import Academy


@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "founded_year", "owner", "contact_email")
    list_filter = ("city", "founded_year")
    search_fields = ("name", "city", "contact_email", "owner__username")
