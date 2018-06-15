from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.
class PastMatchModel(models.Model):
    matches = JSONField()


class CurrentMatchModel(models.Model):
    match_details = JSONField()


class FutureMatchModel(models.Model):
    matches = JSONField()
