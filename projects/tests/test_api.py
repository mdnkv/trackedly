from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from projects.models import Project
from projects.serializers import ProjectListSerializer

from faker import Faker

User = get_user_model()
faker = Faker()


class ProjectAPITest(APITestCase):

    def test_project_create_api_view_creates_project(self):
        """
        Verify that ProjectCreateAPIView creates a new project for a current user
        """
        data = {'name': 'some project', 'is_billable': False, 'weekly_goal': 10, 'customer': ''}
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        self.client.force_authenticate(user=user)
        url = reverse('projects:project_create_api_view')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = Project.objects.filter(owner=user).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, data.get('name'))
        self.assertEqual(result.weekly_goal, data.get('weekly_goal'))
        self.assertFalse(result.is_billable)

    def test_project_update_api_view_only_owner(self):
        """
        Verify that ProjectUpdateAPIView can update only a project that belongs to a current user or 404 returned
        """
        user1 = User.objects.create_user(email=faker.email(), password=faker.password())
        project = Project.objects.create(name='some project', owner=user1)
        user2 = User.objects.create_user(email=faker.email(), password=faker.password())
        self.client.force_authenticate(user=user2)
        data = {'name': 'some project', 'is_billable': False, 'weekly_goal': 10, 'customer': ''}
        url = reverse('projects:project_update_api_view', kwargs={'pk': project.pk})
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_update_api_view_updates_project(self):
        """
        Verify that ProjectUpdateAPIView updates a project
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        project = Project.objects.create(name='some project', owner=user)
        self.client.force_authenticate(user=user)
        data = {'name': 'new project', 'is_billable': True, 'weekly_goal': 10, 'customer': ''}
        url = reverse('projects:project_update_api_view', kwargs={'pk': project.pk})
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = Project.objects.get(id=project.id)
        self.assertEqual(result.name, data.get('name'))
        self.assertEqual(result.weekly_goal, data.get('weekly_goal'))
        self.assertTrue(result.is_billable)

    def test_project_delete_api_view_only_owner(self):
        """
        Verify that ProjectDeleteAPIView can delete only a project that belongs to a current user or 404 returned
        """
        user1 = User.objects.create_user(email=faker.email(), password=faker.password())
        project = Project.objects.create(name='some project', owner=user1)
        user2 = User.objects.create_user(email=faker.email(), password=faker.password())
        self.client.force_authenticate(user=user2)
        url = reverse('projects:project_delete_api_view', kwargs={'pk': project.pk})
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_delete_api_view_deletes_project(self):
        """
        Verify that ProjectDeleteAPIView deletes a project
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        project = Project.objects.create(name='some project', owner=user)
        self.client.force_authenticate(user=user)
        url = reverse('projects:project_delete_api_view', kwargs={'pk': project.pk})
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        result = Project.objects.filter(id=project.id).exists()
        self.assertFalse(result)

    def test_projects_list_api_view_returns_projects(self):
        """
        Verify that ProjectsListAPIView returns a list of projects that belong to a current user
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        Project.objects.create(name='some project', owner=user)
        Project.objects.create(name='some project', owner=user)
        Project.objects.create(name='some project', owner=user)
        self.client.force_authenticate(user=user)
        url = reverse('projects:projects_list_api_view')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProjectListSerializer(data=response.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(response.data), Project.objects.filter(owner=user).count())
