from rest_framework import generics
from entries.models import Entry
from entries.serializers import (EntryListSerializer, EntryCreateSerializer)


class EntryCreateAPIView(generics.CreateAPIView):
    serializer_class = EntryCreateSerializer


class EntryUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EntryCreateSerializer

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class EntryListAPIView(generics.ListAPIView):
    serializer_class = EntryListSerializer

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class EntryDeleteAPIView(generics.DestroyAPIView):

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)
