from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index page'),
    path('shorten', views.shorten_url, name='shorten url'),
    path('<url_key>', views.revert_url, name='redirect to original url')
]