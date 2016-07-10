# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.views import generic
from rest_framework.decorators import api_view
from .models import GuildEvent, New, ThreadImage, PostImage, Post, User, Thread
from django.contrib.auth.models import User
from .permission import PostUserCanEditPermission
from django.contrib.auth import authenticate, login, logout

from .serializers import GuildEventSerializer, NewSerializer, NewAndGuildEventSerializer, ThreadImageSerializer, PostImageSerializer, UserSerializer, PostSerializer, ThreadSerializer
# Create your views here.


def index_view(request):
    return render(request, 'home/home/index.html')


def event_view(request, pk):
    return render(request, 'home/events/events.html')


def event_list_view(request):
    return render(request, 'home/events/events_list.html')


def news_view(request, pk):
    return render(request, 'home/news/news.html')


def news_list_view(request):
    return render(request, 'home/news/news_list.html')


def auth_login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'home/home/index.html', {'login': True})
        else:
            return render(request, 'home/home/index.html', {'login': False})

    return render(request, 'home/home/index.html', {'login': False})

def auth_logout_view(request):
    logout(request)
    return render(request, 'home/home/index.html', {'logout': True})

class UserList(generics.ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class GuildEventList(generics.ListCreateAPIView):
    model = GuildEvent
    queryset = GuildEvent.objects.order_by('-pub_date')
    serializer_class = GuildEventSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class GuildEventDetail(generics.RetrieveUpdateDestroyAPIView):
    model = GuildEvent
    queryset = GuildEvent.objects.all()
    serializer_class = GuildEventSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class NewsList(generics.ListCreateAPIView):
    model = New
    queryset = New.objects.order_by('-pub_date')
    serializer_class = NewSerializer
    permission_classes = [
        permissions.AllowAny
    ]


@api_view(['GET'])
def news_and_guild_event_list(request):
    queryset = sorted(chain(New.objects.all(), GuildEvent.objects.all()), key=attrgetter('pub_date'))[:5]
    print (queryset)
    serializer = []
    for obj in queryset:
        serializer.append(NewAndGuildEventSerializer(obj).data)

    return Response(serializer)


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    model = New
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class ThreadList(generics.ListCreateAPIView):
    model = Thread
    queryset = Thread.objects.order_by('-pub_date')
    serializer_class = ThreadSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class ThreadsImageList(generics.ListCreateAPIView):
    model = ThreadImage
    queryset = ThreadImage.objects.all()
    serializer_class = ThreadImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ThreadsImageDetail(generics.RetrieveUpdateDestroyAPIView):
    model = ThreadImage
    queryset = ThreadImage.objects.all()
    serializer_class = ThreadImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ThreadImageList(generics.ListAPIView):
    model = ThreadImage
    queryset = ThreadImage.objects.all()
    serializer_class = ThreadImageSerializer

    def get_queryset(self):
        queryset = super(ThreadImageList, self).get_queryset()
        return queryset.filter(thread__pk=self.kwargs.get('thread_pk'))


class PostsImageList(generics.ListCreateAPIView):
    model = PostImage
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PostsImageDetail(generics.RetrieveUpdateDestroyAPIView):
    model = PostImage
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PostImageList(generics.ListAPIView):
    model = PostImage
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_queryset(self):
        queryset = super(PostImageList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('post_pk'))


class PostList(generics.ListCreateAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ThreadPostList(generics.ListAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(ThreadPostList, self).get_queryset()
        return queryset.filter(thread__pk=self.kwargs.get('thread_pk'))


class ThreadPostDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(ThreadPostDetail, self).get_queryset()
        return queryset.filter()


class UserPostList(generics.ListAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(user__username=self.kwargs.get('username'))


class PostMixin(object):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        PostUserCanEditPermission
    ]

    def perform_create(self, serializer):
        """Force author to the current user on save"""
        serializer.save(user=self.request.user)


class PostList(PostMixin, generics.ListCreateAPIView):
    pass


class PostDetail(PostMixin, generics.RetrieveUpdateDestroyAPIView):
    pass