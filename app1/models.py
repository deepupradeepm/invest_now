from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=30)
    location=models.CharField(max_length=40)
    share_price=models.IntegerField()

class Invest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    noofsahes=models.IntegerField(default=False)
    company_name=models.ForeignKey(Company,on_delete=models.CASCADE)

class Common_User(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    invested=models.IntegerField()

