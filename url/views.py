import logging
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from url.models import Url, ResultModel
from url.serializer import UrlSerializer, ResultModelSerializer
from url.utils import *

logger = logging.getLogger(__name__)


@api_view(['GET'])
def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def shorten_url(request):
    response = ResultModel()
    try:
        url = make_url_scheme(request.data["url"])

        if not check_valid_domain(url):
            response.result_code = -1
            response.result_msg = "유효하지 않은 url 값입니다. 다시 확인해 주세요."
            return Response(ResultModelSerializer(response).data)

        url_object = get_or_none(Url, original_url=url)

        if url_object is None:
            url_object = Url(shortend_url=make_shorten_url(), original_url=url)
            url_object.save()

        serializer = UrlSerializer(url_object)
        response.data = serializer.data
    except Exception as e:
        response.result_code = -99
        response.result_msg = "잠시 후 다시 시도해주세요."
        logger.error(e)
    return Response(ResultModelSerializer(response).data)


@api_view(['GET'])
def revert_url(request, url_key):
    url = get_shorten_url(url_key)
    try:
        url_object = get_or_none(Url, shortend_url=url)

        if not check_url_key_valid(url_key) or url_object is None:
            return render(request, 'error/404.html')

        url = url_object.original_url
        url_object.clicked_count += 1
        url_object.save()

    except Exception as e:
        logger.error(e)
        return render(request, 'error/500.html')

    return redirect(url)
