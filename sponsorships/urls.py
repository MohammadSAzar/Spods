from django.urls import path

from . import views


urlpatterns = [
    path('registration/content-maker/', views.registration_cm_view, name='registration_cm'),
    path('registration/business-owner/', views.registration_bo_view, name='registration_bo'),
    path('verification/', views.verification_view, name='verification'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/channel/', views.dashboard_channel_view, name='dashboard_channel'),
    path('dashboard/positions/', views.dashboard_positions_view, name='dashboard_positions'),
    path('dashboard/requests/', views.dashboard_requests_view, name='dashboard_requests'),
    path('dashboard/history/', views.dashboard_history_view, name='dashboard_history'),
]



