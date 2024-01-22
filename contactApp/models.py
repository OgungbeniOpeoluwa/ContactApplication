from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)


class Contacts(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    is_blocked = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
