from django import forms
from .models import ReservationSchedule, CustomUser
from django.contrib.auth.forms import UserCreationForm


class ResScheduleForm(forms.ModelForm):
    class Meta:
        model = ReservationSchedule
        fields = ("lib_branch", "res_slot",)
        labels = {
            "lib_branch": "Library Branch",
            "res_slot": "Reservation Slot",
        }


class UserProfileForm(forms.ModelForm):
    initial_fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields["username"].disabled = True

        for key in self.initial_fields:
            if hasattr(user, key):
                self.fields[key].initial = getattr(user, key)

    class Meta:
        model = CustomUser
        fields = ("username", "full_name", "tum_id", "email")
        labels = {
            "full_name": "Full name",
            "tum_id": "TUM ID",
        }
        # Else username will read "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        help_texts = {
            'username': None,
        }


