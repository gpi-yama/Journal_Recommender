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
