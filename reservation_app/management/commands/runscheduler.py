from django.core.management import BaseCommand
from .common.app import App
from reservation_app.models import ReservationSchedule
from django.utils import timezone
import time
import datetime


class Command(BaseCommand):

    last_update = datetime.datetime.now()

    def handle(self, *args, **options):
        app = App("https://www.ub.tum.de/arbeitsplatz-reservieren")
        while True:
            for res_sched in ReservationSchedule.objects.all()[::-1]:

                info = app.make_reservation({
                    "branch_name": res_sched.lib_branch,
                    "time_slot": res_sched.res_slot,
                    "full_name": res_sched.owner.full_name,
                    "tum_id": res_sched.owner.tum_id,
                    "tum_email": res_sched.owner.email,
                }, current_reservation=res_sched.current_res_slot)
                if info["success"]:
                    res_sched.current_res_slot = info["reservation_datetime"]
                    res_sched.save()

            if datetime.datetime.now() - self.last_update > datetime.timedelta(minutes=10.):
                print("Still online...")
                self.last_update = datetime.datetime.now()

        app.teardown()
