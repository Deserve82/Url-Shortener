import random
import logging
from urllib.parse import urlparse

from django.conf import settings

from url.models import Url


logger = logging.getLogger(__name__)


def get_or_none(class_model, **kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.MultipleObjectsReturned as e:
        logger.error(e)
        return None
    except class_model.DoesNotExist:
        return None


def make_shorten_url():
    chars = settings.VALID_CHARS
    while True:
        new_url_key = "".join(random.sample(chars, 8))
        url = get_shorten_url(new_url_key)
        if get_or_none(Url, shortend_url=url) is not None:
            continue
        else:
            break
    return url


def make_url_scheme(url):
    """
    url에 scheme이 없다면 문자열로 붙여주는 함수입니다. 유효하지 않은 형식이라면 빈 문자열을 반환합니다.
    :param: string
    :return: string
    """
    result = url.split("://")
    # scheme을 입력 받지 않았다면 http를 기본으로 붙여줍니다.
    if len(result) == 1:
        url = "http://" + url

    # scheme이 유효하지 않아도 http로 변경해서 넣어줍니다.
    elif len(result) == 2:
        if result[0] not in settings.URL_SCHEMES:
            url = "http://" + result[1]

    # 2개가 아니라면 유효하지 않음으로 빈 문자열을 반환합니다.
    else:
        url = ""
    return url


def check_valid_domain(url):
    result = urlparse(url)
    if result.netloc == "" or result.netloc == settings.CURRENT_DOMAIN:
        return False
    return True


def get_current_url():
    return settings.CURRENT_SCHEME + "://" + settings.CURRENT_DOMAIN


def get_shorten_url(url_key):
    return settings.CURRENT_SCHEME + "://" + settings.CURRENT_DOMAIN + "/" + url_key


def check_url_key_valid(url_key):
    result = True
    if len(url_key) != 8:
        result = False

    for char in url_key:
        if char not in settings.VALID_CHARS:
            result = False
            break

    return result
