from django.db import models
from django.utils import timezone
import datetime
#from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    alpha = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabetic characters are allowed.')
    full_name = models.CharField(max_length=30, validators=[alpha])
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    tum_id = models.CharField(max_length=10, validators=[alphanumeric])
    # USERNAME_FIELD and assword are required by default
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}'s profile"


class LibBranches(models.TextChoices):
    stammgelaende = "Stammgelände"


class LibSlots(models.TextChoices):
    morning = "Morning"
    evening = "Evening"


class ReservationSchedule(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lib_branch = models.CharField(max_length=50, choices=LibBranches.choices, default=LibBranches.stammgelaende)
    res_slot = models.CharField(max_length=50, choices=LibSlots.choices, default=LibSlots.morning)
    pub_datetime = models.DateTimeField("Datetime published")

    def __str__(self):
        return f"ResSchedule: {self.lib_branch} - {self.owner} - {self.res_slot}"

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_datetime <= now


class Reservation(models.Model):
    # Is related to exactly one ReservationSchedule
    schedule = models.ForeignKey(ReservationSchedule, on_delete=models.CASCADE)
    res_datetime = models.DateTimeField("Datetime of reservation")
    creation_datetime = models.DateTimeField("Datetime of creation")

    def __str__(self):
        return f"Res: {self.schedule.lib_branch} - {self.schedule.owner} - {self.res_datetime}"

    def is_soon(self, days=5):
        now = timezone.now()
        return timezone.now() <= self.creation_datetime <= now + datetime.timedelta(days=days)


class BackendError(models.Model):
    caused_by = models.TextField("Error cause")
    info_text = models.TextField("Info")
    at_time = models.DateTimeField("At datetime")
