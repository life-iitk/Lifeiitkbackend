from django.db import models


from users.models.users import User
from tags.models import TagModel
# Create your models here.


class privileges(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tag = models.ForeignKey(TagModel, on_delete=models.CASCADE)
