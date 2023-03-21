from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=50)
    # dob = models.DateField()
    email = models.EmailField(max_length=254,unique=True)
    mobile_number = PhoneNumberField()
    profile_pic = models.ImageField(upload_to='profile_pictures',blank=True)
    gender = models.CharField(max_length=10)
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    # @property
    # def age(self):
    #     today = date.today()
    #     age = today.year-self.dob.year
    #     if today.month < self.dob.month or today.month == self.dob.month and today.day<self.dob.day:
    #         age-=1
    #     return age

class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=True)
    name = models.CharField(max_length = 50)
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    mobile_number = PhoneNumberField()
    gender = models.CharField(max_length = 10)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)
    profile_pic = models.ImageField(upload_to='profile_pictures',blank=True)
    registration_no = models.CharField(max_length = 20)
    year_of_registration = models.DateField()
    qualification = models.CharField(max_length = 20)
    Medical_Council = models.CharField(max_length = 30)

    specialization = models.CharField(max_length = 30)

    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    def get_url(self):
        return reverse('products_by_category', args=[self.slug,])
    @property
    def age(self):
        today = date.today()
        age = today.year-self.dob.year
        if today.month < self.dob.month or today.month == self.dob.month and today.day<self.dob.day:
            age-=1
        return age
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Doctor, self).save(*args, **kwargs)
    
class Feedback(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Patient,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,null=True)
    feedback = models.TextField()
    
    def __unicode__(self):
        return self.feedback