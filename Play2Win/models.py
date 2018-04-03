from django.db import models
from .models import *
from django.contrib.auth.models import *
import datetime
# Models are created here
class Player(models.Model):
    developer = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def method_example(self):
        pass
