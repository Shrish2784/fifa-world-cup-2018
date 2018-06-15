from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.PastMatchModel)
admin.site.register(models.CurrentMatchModel)
admin.site.register(models.FutureMatchModel)
