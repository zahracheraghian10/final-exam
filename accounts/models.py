from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    phone = models.CharField(verbose_name="Phone Number ", max_length=11)

        
# Create your models here.
