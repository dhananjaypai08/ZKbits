from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.TextField(default=False)
    
        
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.TextField(default=False)