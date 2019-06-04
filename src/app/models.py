from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(max_length=100)
    author = models.TextField()
    abstract = models.TextField()
    date = models.Field()
    url = models.TextField()
    jname = models.TextField()

    class Meta:
        managed = False
        db_table = "items"


class PostFav(models.Model):
    fav_id = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fav_date = models.DateTimeField(
        default=datetime.now
    )
    score = models.IntegerField(default=0)

    class Meta:
        db_table = "favorite"


class RecomSim(models.Model):
    id = models.IntegerField(primary_key=True)
    rank1 = models.IntegerField()
    rank2 = models.IntegerField()
    rank3 = models.IntegerField()
    rank4 = models.IntegerField()
    rank5 = models.IntegerField()
    rank6 = models.IntegerField()
    rank7 = models.IntegerField()
    rank8 = models.IntegerField()
    rank9 = models.IntegerField()
    rank10 = models.FloatField()
    score1 = models.FloatField()
    score2 = models.FloatField()
    score3 = models.FloatField()
    score4 = models.FloatField()
    score5 = models.FloatField()
    score6 = models.FloatField()
    score7 = models.FloatField()
    score8 = models.FloatField()
    score9 = models.FloatField()
    score10 = models.FloatField()

    class Meta:
        managed=False
        db_table = "similality"

