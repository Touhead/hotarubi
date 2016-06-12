from django.conf.urls import url, include
from . import views
from django.conf import settings

app_name = 'home'

event_urls = [
    url(r'(?P<pk>\d+)$', views.GuildEventDetail.as_view(), name='guild-event-detail'),
    url(r'$', views.GuildEventList.as_view(), name='guild-event-list')
]

news_urls = [
    url(r'(?P<pk>\d+)$', views.NewDetail.as_view(), name='news-detail'),
    url(r'$', views.NewList.as_view(), name='news-list')
]

urlpatterns = [
    url(r'^home$', views.IndexView.as_view(), name='index'),
    url(r'^api/events', include(event_urls)),
    url(r'^api/news', include(news_urls))
]