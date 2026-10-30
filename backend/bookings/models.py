from django.db import models

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ("Consultation", "Consultation"),
        ("Project Discussion", "Project Discussion"),
        ("Career Guidance", "Career Guidance"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=40, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]
        constraints = [
            models.UniqueConstraint(fields=["date", "time"], name="unique_appointment_date_time")
        ]

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
