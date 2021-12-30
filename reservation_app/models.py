from django.db import models
from django.utils import timezone
import datetime


class LibBranches(models.TextChoices):
    stamm = "Stammgelände"


class LibSlots(models.TextChoices):
    morning = "Morning"
    evening = "Evening"


class ReservationSchedule(models.Model):
    lib_branch = models.CharField(max_length=50, choices=LibBranches.choices, default=LibBranches.stamm)
    res_slot = models.CharField(max_length=50, choices=LibSlots.choices, default=LibSlots.morning)
    pub_date = models.DateTimeField("Datetime published")

    def __str__(self):
        return f"ResSchedule: {self.lib_branch} - {self.res_datetime} - {self.res_slot}"

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Reservation(models.Model):
    # Is related to exactly one ReservationSchedule
    schedule = models.ForeignKey(ReservationSchedule, on_delete=models.CASCADE)
    res_datetime = models.DateTimeField("Datetime of reservation")
    creation_datetime = models.DateTimeField("Datetime of creation")

    def __str__(self):
        return f"Res: {self.schedule.lib_branch} - {self.res_datetime} - {self.schedule.res_slot}"

    def is_soon(self, days=5):
        now = timezone.now()
        return timezone.now() <= self.res_datetime <= now + datetime.timedelta(days=days)
