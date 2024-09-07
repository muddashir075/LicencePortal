from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    #username = models.CharField(max_length=50)
    #password = models.EmailField(unique=True)
    ROLE_CHOICES = (('resourse', 'Resourse'),
                    ('manager', 'Manager'),
                    ('admin', 'Admin'),)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resource')

class Licence_Data(models.Model):
    #ADMIN = 'ADMIN'
    #MANAGER = 'MANAGER'
    #USER = 'USER'
    #usertype = [(ADMIN,'ADMIN'), (MANAGER,'MANAGER'),(USER,'USER')]
    id = models.AutoField(primary_key=True)
    #user_type = models.CharField(max_length=10, choices=usertype, default='USER')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    pdf= models.FileField(upload_to='documents')
    
    def __str__(self):
        return self.name
    