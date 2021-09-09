from django.urls import path
from . import views

urlpatterns = [
    path('apt_requests/', views.AppointmentListView.as_view(), name='apt_requests'),
    path('accepted_apts/', views.AcceptedAppointmentListView.as_view(), name='accepted_apts'),
    path('pending_apts/', views.PendingAppointmentListView.as_view(), name='pending_apts'),
    # path('update_apt/', views.AppointmentUpdateView.as_view(), name='pending_apts'),
    path('apt_status/<int:pk>/<str:status>/', views.update_appointment_status, name='apt_status'),
    path('apt_status_res/<int:pk>/<str:status>/', views.update_appointment_response_status, name='apt_status_res'),
    path('appointment_response/<int:pk>', views.AppointmentResponseView.as_view(), name='appointment_response'),
    path('all_users/', views.AllUsersList.as_view(), name='all_users'),
    path('user_appointments/<int:pk>', views.UserAppointments.as_view(), name='user_appointments'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('get_month/<int:month>/', views.get_month_num, name='get_month'),
]