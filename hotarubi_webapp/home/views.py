from django.http import HttpResponse
from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.views import generic
from rest_framework.decorators import api_view
from .models import GuildEvent, New
from .serializers import EventsSerializer, NewSerializer, NewAndGuildEventSerializer
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'latest_event_list'

    def get_queryset(self):
        return GuildEvent.objects.order_by('-pub_date')[:5]


class GuildEventList(generics.ListCreateAPIView):
    model = GuildEvent
    queryset = GuildEvent.objects.order_by('-pub_date')[:5]
    serializer_class = EventsSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class GuildEventDetail(generics.RetrieveUpdateDestroyAPIView):
    model = GuildEvent
    queryset = GuildEvent.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class NewList(generics.ListCreateAPIView):
    model = New
    queryset = New.objects.order_by('-pub_date')[:5]
    serializer_class = NewSerializer
    permission_classes = [
        permissions.AllowAny
    ]


@api_view(['GET'])
def new_and_guild_event_list(request):
    queryset = sorted(chain(New.objects.all(), GuildEvent.objects.all()), key=attrgetter('pub_date'))[:5]
    print (queryset)
    serializer = []
    for obj in queryset:
        serializer.append(NewAndGuildEventSerializer(obj).data)

    return Response(serializer)


class NewDetail(generics.RetrieveUpdateDestroyAPIView):
    model = New
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [
        permissions.AllowAny
    ]