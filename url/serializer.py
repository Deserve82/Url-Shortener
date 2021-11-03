from rest_framework import serializers
from .models import Url


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['original_url', 'shortend_url', 'clicked_count']


class ResultModelSerializer(serializers.Serializer):
    result_code = serializers.IntegerField()
    result_msg = serializers.CharField(max_length=1000)
    data = serializers.JSONField()
