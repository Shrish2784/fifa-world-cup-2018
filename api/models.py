from django.db import models

# Create your models here.
class Match(models.Model):
    matches = models.CharField(max_length=20000, null=True)
