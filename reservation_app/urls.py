from django.urls import path

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("home/", views.HomeView.as_view(), name='home'),
    path("booking/", views.BookingView.as_view(), name="booking"),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name="user_profile"),
    path(r'delete/<int:pk>/$', views.DeleteView.as_view(), name='delete_sched'),
]
