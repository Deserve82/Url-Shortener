import random

from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from url.models import Url
from url.serializer import UrlSerializer


def convert():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while True:
        new_url = "".join(random.sample(chars, 8))
        try:
            Url.objects.get(shortend_url=new_url)
        except:
            return new_url


@api_view(['GET'])
def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def shorten_url(request):
    try:
        url = Url.objects.get(original_url=request.data["url"])
        serializer = UrlSerializer(url)
        return Response(serializer.data)
    except:
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_shortend_url = convert()
            new_url = request.scheme + "://" + request.get_host() + "/" + new_shortend_url
            serializer.save(shortend_url=new_url, original_url=request.data["url"])
            return Response(serializer.data)


@api_view(['GET'])
def revert_url(request, url_key):
    url = Url.objects.get(shortend_url=request.scheme + "://" + request.get_host() + "/" + url_key)
    return redirect(request.scheme + "://" + url.original_url)
