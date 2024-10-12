from django.urls import path

from . import views


urlpatterns = [
    path('registration/content-maker/', views.registration_cm_view, name='registration_cm'),
    path('registration/business-owner/', views.registration_bo_view, name='registration_bo'),
    path('verification/', views.verification_view, name='verification'),
]



