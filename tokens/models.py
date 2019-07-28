from django.db import models
from users.models.users import User

# Create your models here.
class Token(models.Model):
    token = models.CharField(primary_key=True,max_length = 100)
    user = models.ManyToManyField(User,related_name="tokens")
