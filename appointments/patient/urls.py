from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('query_appointment/', views.CreateAppointmentView.as_view(), name='query_appointment'),
    path('appointment_response/<int:pk>', views.AppointmentResponseView.as_view(), name='appointment_response'),
]
