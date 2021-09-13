from django.urls import path
from . import views

urlpatterns = [
    path('apt_requests/', views.AppointmentListView.as_view(), name='apt_requests'),
    path('accepted_apts/', views.AcceptedAppointmentListView.as_view(), name='accepted_apts'),
    path('pending_apts/', views.PendingAppointmentListView.as_view(), name='pending_apts'),
    path('update_apt/<int:pk>/', views.AppointmentUpdateView.as_view(), name='update_apt'),
    path('update_apt_res/<int:pk>/', views.AppointmentResponseUpdateView.as_view(), name='update_apt_res'),
    path('apt_status/<int:pk>/<str:status>/', views.update_appointment_status, name='apt_status'),
    path('apt_status_res/<int:pk>/<str:status>/', views.update_appointment_response_status, name='apt_status_res'),
    path('appointment_response/<int:pk>', views.AppointmentResponseView.as_view(), name='appointment_response'),
    path('all_users/', views.AllUsersList.as_view(), name='all_users'),
    path('user_appointments/<int:pk>', views.UserAppointments.as_view(), name='user_appointments'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('delete_appointment/<int:pk>', views.delete_appointment, name='delete_appointment'),
    path('delete_appointment_response/<int:pk>', views.delete_appointment_response, name='delete_appointment_response'),
    path('create_appoint/<int:year>/<int:month>/<int:day>/', views.TherapistCreateAppointmentView.as_view(), name='create_appoint'),
    path('disable_day/<int:pk>/', views.disable_day, name='disable_day'),
    path('enable_day/<int:pk>/', views.enable_day, name='enable_day'),
    # path('days/', views.DisableDaysListView.as_view(), name='disable_days_list'),
    path('working_time/', views.WorkingTimeView.as_view(), name='working_time'),
    path('preferences/', views.PreferencesView.as_view(), name='preferences'),
]