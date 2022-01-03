from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import ResScheduleForm, UserProfileForm
from .models import ReservationSchedule, Reservation, CustomUser
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class HomeView(generic.TemplateView):
    template_name = 'reservation_app/home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        cntx_d = {"all_ResSched_list": []}
        if user.is_authenticated:
            cntx_d["all_ResSched_list"] = ReservationSchedule.objects.filter(owner=self.request.user)
        return cntx_d


class BookingView(LoginRequiredMixin, generic.FormView):
    template_name = "reservation_app/booking.html"
    form_class = ResScheduleForm
    success_url = reverse_lazy("booking")
    permission_denied_message = "Cannot add schedule."

    def form_valid(self, form):
        # Save the form, but do not save the model yet
        res_schedule = form.save(commit=False)
        res_schedule.owner = self.request.user
        res_schedule.pub_datetime = timezone.now()
        # Save the model to the database
        if not self.check_duplicate(res_schedule.owner, res_schedule.lib_branch, res_schedule.res_slot):
            res_schedule.save()
        return super(BookingView, self).form_valid(form)

    @staticmethod
    def check_duplicate(owner, branch, slot):
        return ReservationSchedule.objects.filter(
            owner=owner,
            lib_branch=branch,
            res_slot=slot,
        ).exists()


class UserProfileView(LoginRequiredMixin, generic.UpdateView):
    template_name = "reservation_app/profile.html"
    form_class = UserProfileForm
    model = CustomUser

    def get_form_kwargs(self):
        """
        https://stackoverflow.com/questions/43237742/django-pass-data-from-cbv-form-view-to-form-cbv
        """
        kwargs = super(UserProfileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        profile = form.save(commit=True)
        self.success_url = reverse("user_profile", args=(self.request.user.pk,))
        return super(UserProfileView, self).form_valid(form)


class DeleteView(SuccessMessageMixin, generic.DeleteView):
    model = ReservationSchedule
    success_url = reverse_lazy("home")
    success_message = "deleted philipp obj"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        pk = obj.pk
        request.session['pk'] = pk  # name will be change according to your need
        message = f'{obj} deleted successfully'
        messages.success(self.request, message)
        return super(DeleteView, self).delete(request, *args, **kwargs)