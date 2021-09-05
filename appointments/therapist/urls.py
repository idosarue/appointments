from django.urls import path
from . import views

urlpatterns = [
    path('apt_requests/', views.AppointmentListView.as_view(), name='apt_requests'),
    path('apt_status/<int:pk>/<str:status>/', views.update_appointment_status, name='apt_status'),
]
