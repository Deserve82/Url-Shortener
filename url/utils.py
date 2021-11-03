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
    result = urlparse(url)
    if result.scheme == "":
        # scheme이 없거나 잘못 되었다면 default로 http를 넣어줍니다.
        url = "http://" + url
    elif result.scheme not in settings.URL_SCHEMES:
        url = "http://" + url.split("://")[1]
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
