from django.contrib import admin
from .models import ReservationSchedule, CustomUser
# Register your models here.

admin.site.register(ReservationSchedule)
admin.site.register(CustomUser)

