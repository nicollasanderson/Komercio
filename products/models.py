from pyexpat import model
from django.db import models

# Create your models here.

class Product(models.Model):
    description = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2,max_digits=9999)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='seller')