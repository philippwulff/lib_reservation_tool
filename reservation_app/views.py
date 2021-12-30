from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import SelectWeekdayForm


class HomeView(generic.TemplateView):
    template_name = 'reservation_app/home.html'

    def get_queryset(self):
        return


class BookingView(generic.FormView):
    template_name = "reservation_app/booking.html"
    form_class = SelectWeekdayForm

    def get_queryset(self):
        return
