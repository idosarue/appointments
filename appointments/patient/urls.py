from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('query_appointment/', views.CreateAppointmentView.as_view(), name='query_appointment'),
    path('query_appointment_update/<int:pk>/', views.CreateAppointmentViewAfterUpdate.as_view(), name='query_appointment_update'),
    path('future_appointments/', views.FutureAppointmentsListView.as_view(), name='future_appointments'),
    path('past_appointments/', views.PastAppointmentsListView.as_view(), name='past_appointments'),
]
