from rest_framework import generics

from projects.models import Project
from projects.serializers import (ProjectListSerializer, ProjectCreateSerializer)


class ProjectCreateAPIView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer


class ProjectUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProjectCreateSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectsListAPIView(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDeleteAPIView(generics.DestroyAPIView):

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
