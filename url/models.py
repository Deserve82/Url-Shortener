import datetime

from django.db import models


class Url(models.Model):
    original_url = models.URLField(default="", max_length=2100, null=False)
    shortend_url = models.URLField(default="", max_length=8, null=False)
    create_at = models.DateTimeField(default=datetime.datetime.now(), null=False)
    clicked_count = models.IntegerField(default=0, null=False)
