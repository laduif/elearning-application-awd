from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import StatusUpdate, User


class AccountTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username='student1',
            password='testpassword123',
            role='STUDENT'
        )

        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpassword123',
            role='TEACHER'
        )

    def test_student_can_login(self):
        logged_in = self.client.login(
            username='student1',
            password='testpassword123'
        )

        self.assertTrue(logged_in)

    def test_teacher_can_access_search(self):
        self.client.force_login(self.teacher)

        response = self.client.get(
            reverse('search')
        )

        self.assertEqual(response.status_code, 200)

    def test_student_cannot_access_search(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse('search')
        )

        self.assertEqual(response.status_code, 302)

    def test_student_can_create_status_update(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse(
                'profile',
                args=[self.student.id]
            ),
            {
                'content': 'This is my test status.'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            StatusUpdate.objects.filter(
                user=self.student,
                content='This is my test status.').exists()
        )


class UserAPITests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username='student1',
            password='testpassword123',
            role='STUDENT'
        )

        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpassword123',
            role='TEACHER'
        )

        self.api_client = APIClient()

    def test_user_list_requires_authentication(self):
        response = self.api_client.get(
            reverse('api_user_list')
        )

        self.assertIn(
            response.status_code,
            [401, 403]
        )

    def test_authenticated_user_can_view_user_list(self):
        self.api_client.force_authenticate(
            user=self.student
        )

        response = self.api_client.get(
            reverse('api_user_list')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.data),
            2
        )

