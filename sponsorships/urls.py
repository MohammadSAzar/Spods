from django.urls import path

from . import views


urlpatterns = [
    path('registration/content-maker/', views.registration_cm_view, name='registration_cm'),
    path('registration/business-owner/', views.registration_bo_view, name='registration_bo'),
    path('verification/', views.verification_view, name='verification'),
    path('dashboard/content-maker/', views.dashboard_cm_view, name='dashboard_cm'),
    path('dashboard/business-owner/', views.dashboard_bo_view, name='dashboard_bo'),
]



