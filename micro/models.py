from django.db import models

# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=10)
    pic = models.CharField(max_length=256)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

