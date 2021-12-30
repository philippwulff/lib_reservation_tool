from django import forms


class SelectWeekdayForm(forms.Form):
    page = forms.ChoiceField(label="Your label", choices=((0, '0'), (5, '5'), (10, "10")), required=True)


