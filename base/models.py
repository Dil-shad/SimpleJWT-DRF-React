from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    body=models.TextField()
    