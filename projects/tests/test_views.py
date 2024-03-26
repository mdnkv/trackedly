from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from faker import Faker

from projects.models import Project

User = get_user_model()
faker = Faker()


class ProjectViewTest(TestCase):

    def test_project_update_view_is_rendered(self):
        """
        Verify that ProjectUpdateView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Project that is owned by the user
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        project = Project.objects.create(name="project1", owner=user)
        url = reverse("projects:project_update_view", kwargs={"pk": project.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/views/project_update_view.html")

    def test_project_update_view_update_only_owned_project(self):
        """
        Verify that user can update only the owned Project object.
        If user tries to call the project update view for Project that belongs to another user,
        the 404 response is returned
        """
        user1 = User.objects.create_user(email=faker.email(), password='secret1234')
        user2 = User.objects.create_user(email=faker.email(), password='secret1234')
        project = Project.objects.create(name="project1", owner=user1)
        self.client.force_login(user2)
        url = reverse("projects:project_update_view", kwargs={"pk": project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_project_update_view_updates_project(self):
        """
        Verify that ProjectUpdateView updates project
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        project = Project.objects.create(name="project1", owner=user)
        url = reverse("projects:project_update_view", kwargs={"pk": project.pk})
        self.client.force_login(user)
        data = {'name': 'new project name', 'is_billable': True, 'customer': '', 'weekly_goal': 0}
        response = self.client.post(url, data)
        result = Project.objects.get(pk=project.pk)
        self.assertEqual(result.name, data['name'])
        self.assertTrue(result.is_billable)

    def test_project_delete_view_is_rendered(self):
        """
        Verify that ProjectDeleteView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Project that is owned by the user
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        project = Project.objects.create(name="project1", owner=user)
        url = reverse("projects:project_delete_view", kwargs={"pk": project.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/views/project_delete_view.html")

    def test_project_delete_view_delete_only_owned_project(self):
        """
        Verify that user can delete only the owned Project object.
        If user tries to call the project delete view for Project that belongs to another user,
        the 404 response is returned
        """
        user1 = User.objects.create_user(email=faker.email(), password='secret1234')
        user2 = User.objects.create_user(email=faker.email(), password='secret1234')
        project = Project.objects.create(name="project1", owner=user1)
        self.client.force_login(user2)
        url = reverse("projects:project_delete_view", kwargs={"pk": project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_project_delete_view_deletes_project(self):
        """
        Verify that ProjectDeleteView deletes the project object
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        project = Project.objects.create(name="project1", owner=user)
        url = reverse("projects:project_delete_view", kwargs={"pk": project.pk})
        self.client.force_login(user)
        response = self.client.post(url)
        result = Project.objects.filter(pk=project.pk).exists()
        self.assertFalse(result)

    def test_project_create_view_is_rendered(self):
        """
        Verify that ProjectCreateView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("projects:project_create_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/views/project_create_view.html")

    def test_project_create_view_creates_project(self):
        """
        Verify that ProjectCreateView creates a new project
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("projects:project_create_view")
        data = {
            'name': 'project',
            'is_billable': True,
            'customer': '',
            'weekly_goal': 0
        }
        self.client.post(url, data)
        result = Project.objects.filter(owner=user).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, data['name'])
        self.assertTrue(result.is_billable)

    def test_projects_list_view_is_rendered(self):
        """
        Verify that ProjectListView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("projects:projects_list_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/views/projects_list_view.html")
