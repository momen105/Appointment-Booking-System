from django.db import models
from core.models import BaseModel
from apps.user.models import *

class DoctorDetails(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, )
    license_number = models.CharField(max_length=100, unique=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Dr. {self.user.full_name} - License: {self.license_number}"

class DoctorAvailability(models.Model):
    WEEKDAYS = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE, related_name='availabilities')
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'weekday', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.get_weekday_display()} {self.start_time} to {self.end_time}"

class Appointment(models.Model):

    status = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='appointments_as_patient', limit_choices_to={'user_type': User.UserType.PATIENT})
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='appointments_as_doctor', limit_choices_to={'user_type': User.UserType.DOCTOR})

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=status, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')

    def __str__(self):
        return f"Appointment {self.id} with Dr. {self.doctor.full_name} on {self.appointment_date} at {self.appointment_time}"

class MonthlyReport(models.Model):
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    month = models.DateField(help_text="First day of the month")
    total_patients = models.PositiveIntegerField()
    total_appointments = models.PositiveIntegerField()
    total_money_earned = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('doctor', 'month')

    def __str__(self):
        return f"Report for Dr. {self.doctor.full_name} - {self.month.strftime('%B %Y')}"