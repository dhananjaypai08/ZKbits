from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=200)
    mode = models.CharField(max_length=200)
    totalamount = models.IntegerField()
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    