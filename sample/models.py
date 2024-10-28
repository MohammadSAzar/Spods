from django.db import models


class TestContentMaker(models.Model):
    title = models.CharField(max_length=500)
    creator = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    cover = models.ImageField(upload_to='pod_covers/')
    subscribers = models.PositiveBigIntegerField()
    played = models.PositiveBigIntegerField()

