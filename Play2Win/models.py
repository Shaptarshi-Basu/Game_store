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
class Game(models.Model):
    game_name = models.CharField(max_length=255)
    game_url = models.URLField()
    game_developer = models.ForeignKey(User,on_delete=models.DO_NOTHING,)
    game_price = models.PositiveIntegerField(default=0)
    game_sales = models.PositiveIntegerField(default=0)
class Score(models.Model):
    game = models.ForeignKey(Game,on_delete=models.DO_NOTHING,)
    player = models.ForeignKey(User,on_delete=models.DO_NOTHING,)
    score = models.PositiveIntegerField(default=0)
    state = models.TextField(blank=True, null=True)
    game_timestamp = models.DateTimeField(auto_now_add=True)
