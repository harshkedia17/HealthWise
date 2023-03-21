from django.urls import path
from .views import *


urlpatterns = [
    path('signup_patient',signup_patient,name='signup_patient'),
    path('signup_doctor',signup_doctor,name='signup_doctor'),
    path('login_patient',login_patient,name='login_patient'),
    path('login_doctor',login_doctor,name='login_doctor'),
    path('logout',logout,name='logout'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
]
