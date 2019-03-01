from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.TextField(max_length=100)
    author = models.TextField()
    abstract = models.TextField()
    date = models.Field()

    class Meta:
        managed = False
        db_table = "items"
