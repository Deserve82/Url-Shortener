import datetime

from django.db import models


class Url(models.Model):
    original_url = models.URLField(default="", max_length=2100, null=False)
    shortend_url = models.URLField(default="", max_length=8, null=False)
    create_at = models.DateTimeField(default=datetime.datetime.now(), null=False)
    clicked_count = models.IntegerField(default=0, null=False)


class ResultModel:
    def __init__(self, result_code=0, message="", data=None):
        self.result_code = result_code
        self.result_msg = message
        self.data = data
