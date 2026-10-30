from django.contrib import admin
from django.urls import path
from bookings import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/slots/", views.available_slots, name="available_slots"),
    path("api/appointments/", views.create_appointment, name="create_appointment"),
]
