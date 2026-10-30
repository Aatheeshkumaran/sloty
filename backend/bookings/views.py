import json
from datetime import datetime, date as date_type
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.utils import timezone
from .models import Appointment

TIME_SLOTS = [
    "09:00", "10:00", "11:00", "12:00",
    "14:00", "15:00", "16:00", "17:00",
]

def available_slots(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    date_value = request.GET.get("date", "")
    try:
        selected_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Please provide a valid date in YYYY-MM-DD format."}, status=400)

    if selected_date < timezone.localdate():
        return JsonResponse({"error": "Please choose today or a future date."}, status=400)

    booked = set(
        Appointment.objects.filter(date=selected_date).values_list("time", flat=True)
    )
    booked_strings = {value.strftime("%H:%M") for value in booked}
    available = [slot for slot in TIME_SLOTS if slot not in booked_strings]

    return JsonResponse({
        "date": selected_date.isoformat(),
        "slots": available,
        "booked_slots": sorted(booked_strings),
    })

@csrf_exempt
def create_appointment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    service = str(data.get("service", "")).strip()
    date_value = str(data.get("date", "")).strip()
    time_value = str(data.get("time", "")).strip()
    notes = str(data.get("notes", "")).strip()

    if not all([name, email, service, date_value, time_value]):
        return JsonResponse({"error": "Please fill in all required fields."}, status=400)
    if len(name) > 100:
        return JsonResponse({"error": "Name must be 100 characters or fewer."}, status=400)
    if service not in dict(Appointment.SERVICE_CHOICES):
        return JsonResponse({"error": "Please choose a valid service."}, status=400)

    try:
        selected_date = datetime.strptime(date_value, "%Y-%m-%d").date()
        selected_time = datetime.strptime(time_value, "%H:%M").time()
    except ValueError:
        return JsonResponse({"error": "Invalid date or time."}, status=400)

    if selected_date < timezone.localdate():
        return JsonResponse({"error": "Appointments cannot be booked in the past."}, status=400)
    if time_value not in TIME_SLOTS:
        return JsonResponse({"error": "That time slot is not available."}, status=400)

    try:
        appointment = Appointment.objects.create(
            name=name,
            email=email,
            service=service,
            date=selected_date,
            time=selected_time,
            notes=notes,
        )
    except IntegrityError:
        return JsonResponse({"error": "Sorry, this slot has just been booked. Please choose another time."}, status=409)

    return JsonResponse({
        "message": "Appointment booked successfully!",
        "appointment": {
            "id": appointment.id,
            "name": appointment.name,
            "service": appointment.service,
            "date": appointment.date.isoformat(),
            "time": appointment.time.strftime("%H:%M"),
        },
    }, status=201)
