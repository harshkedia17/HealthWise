from django.contrib import admin
from .models import *
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
# Register your models here.

class PatientForm(forms.ModelForm):
    class Meta:
        widgets = {
            'mobile_number' :PhoneNumberPrefixWidget(initial='US'),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        widgets = {
            'mobile_number' :PhoneNumberPrefixWidget(initial='US'),
        }

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    form = PatientForm
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorForm