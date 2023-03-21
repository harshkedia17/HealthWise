
# Create your models here.
from django.db import models
from accounts.models import Doctor, User

class Symptoms(models.Model):
    symptom_name = models.CharField(max_length=100)
    
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number  = models.CharField(max_length=10)
    email = models.EmailField()
    date = models.DateField( auto_now=False, auto_now_add=False)
    time = models.TimeField( auto_now=False, auto_now_add=False)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=50)