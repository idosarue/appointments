from datetime import date
from django.urls import path
from . import views

urlpatterns = [
    path('apt_requests/', views.AppointsRequestsView.as_view(), name='apt_requests'),
    path('pending_apts/', views.PendingAppointsView.as_view(), name='pending_apts'),
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
    path('create_appoint/', views.TherapistCreateAppointmentView.as_view(), name='create_appoint'),
    path('get_date_f/<int:year>/<int:month>/<int:day>/', views.get_date_f, name='get_date_f'),
    path('disable_day/<int:pk>/', views.disable_day, name='disable_day'),
    path('enable_day/<int:pk>/', views.enable_day, name='enable_day'),
    path('disable_date/', views.DisableDatesView.as_view(), name='disable_dates'),
    path('enable_date/<int:pk>/', views.enable_date, name='enable_date'),
    path('working_time/', views.WorkingTimeView.as_view(), name='working_time'),
    path('preferences/', views.PreferencesView.as_view(), name='preferences'),
    path('appoint_list/', views.AppointsView.as_view(), name='appoint_list'),
    path('create_comment/', views.CreateCommentView.as_view(), name='create_comment'),
    # path('edit_comment/<int:pk>/', views.EditCommentView.as_view(), name='edit_comment'),
    path('edit_comment/', views.EditCommentView.as_view(), name='edit_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
]