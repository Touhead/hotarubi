# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views

from django.conf import settings

app_name = 'home'

event_urls = [
    url(r'(?P<pk>\d+)$', views.event_view, name='event-detail-page'),
    url(r'$', views.event_list_view, name='event-list-page'),
]

new_urls = [
    url(r'(?P<pk>\d+)$', views.news_view, name='new-detail-page'),
    url(r'$', views.news_list_view, name='new-detail-page')
]

auth_urls = [
    url(r'login$', views.auth_login_view, name='auth-page'),
    url(r'logout$', views.auth_logout_view, name='auth-page')
]

api_user_urls = [
    url(r'(?P<username>[0-9a-zA-Z_-]+)/posts$', views.UserPostList.as_view(), name='user-post-list'),
    url(r'(?P<username>[0-9a-zA-Z_-]+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'$', views.UserList.as_view(), name='user-list')
]

api_thread_urls = [
    url(r'(?P<thread_pk>\d+)/images$', views.ThreadImageList.as_view(), name='thread-image-list'),
    url(r'(?P<thread_pk>\d+)/posts/(?P<pk>\d+)$', views.ThreadPostDetail.as_view(), name='thread-post-detail'),
    url(r'(?P<thread_pk>\d+)/posts$', views.ThreadPostList.as_view(), name='thread-post-list'),
    url(r'$', views.ThreadList.as_view(), name='thread-list')
]

api_event_urls = [
    url(r'(?P<pk>\d+)/images$', views.ThreadImageList.as_view(), name='event-image-list'),
    url(r'(?P<pk>\d+)$', views.GuildEventDetail.as_view(), name='guild-event-detail'),
    url(r'$', views.GuildEventList.as_view(), name='guild-event-list')
]

api_new_urls = [
    url(r'(?P<pk>\d+)/images$', views.ThreadImageList.as_view(), name='event-image-list'),
    url(r'(?P<pk>\d+)$', views.NewsDetail.as_view(), name='new-detail'),
    url(r'$', views.NewsList.as_view(), name='new-list')
]

api_thread_image_urls = [
    url(r'(?P<pk>\d+)$', views.ThreadsImageDetail.as_view(), name='image-detail'),
    url(r'$', views.ThreadsImageList.as_view(), name='image-list')
]

api_post_image_urls = [
    url(r'(?P<pk>\d+)$', views.PostsImageDetail.as_view(), name='image-detail'),
    url(r'$', views.PostsImageList.as_view(), name='image-list')
]

api_post_urls = [
    url(r'(?P<post_pk>\d+)/images$', views.PostImageList.as_view(), name='post-image-list'),
    url(r'(?P<pk>\d+)$', views.PostDetail.as_view(), name='post-detail'),
    url(r'$', views.PostList.as_view(), name='post-list')
]

urlpatterns = [
    url(r'^events', include(event_urls)),
    url(r'^news', include(new_urls)),
    url(r'^auth', include(auth_urls)),
    url(r'^api/threads', include(api_thread_urls)),
    url(r'^api/events', include(api_event_urls)),
    url(r'^api/news', include(api_new_urls)),
    url(r'^api/images/thread/', include(api_thread_image_urls)),
    url(r'^api/images/post/', include(api_post_image_urls)),
    url(r'^api/posts', include(api_post_urls)),
    url(r'^api/users', include(api_user_urls)),
    url(r'^$', views.index_view, name='index'),
]