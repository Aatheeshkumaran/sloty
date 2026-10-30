from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "date", "time", "created_at")
    list_filter = ("service", "date")
    search_fields = ("name", "email")
    date_hierarchy = "date"
