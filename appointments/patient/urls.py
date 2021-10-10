from django.urls import path
from . import views



urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.CreateContactMessageToTherapist.as_view(), name='home'),
    path('query_appointment/', views.CreateAppointmentView.as_view(), name='query_appointment'),
    path('query_appointment_update/<int:pk>/', views.CreateAppointmentViewAfterUpdate.as_view(), name='query_appointment_update'),
    path('appointments/', views.AppointsListView.as_view(), name='appointments'),
]
