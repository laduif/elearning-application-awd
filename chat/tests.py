from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from courses.models import BlockStudent, Course, Enrolment


class ChatTests(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpassword123',
            role='TEACHER'
        )

        self.student = User.objects.create_user(
            username='student1',
            password='testpassword123',
            role='STUDENT'
        )

        self.other_student = User.objects.create_user(
            username='student2',
            password='testpassword123',
            role='STUDENT'
        )

        self.course = Course.objects.create(
            title='Web Development',
            description='Test course.',
            teacher=self.teacher
        )

        Enrolment.objects.create(
            student=self.student,
            course=self.course
        )

    def test_teacher_can_access_course_chat(self):
        self.client.force_login(self.teacher)

        response = self.client.get(
            reverse(
                'chat_room',
                args=[self.course.id]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_enrolled_student_can_access_course_chat(self):
        self.client.force_login(self.student)

        response = self.client.get(
            reverse(
                'chat_room',
                args=[self.course.id]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_non_enrolled_student_cannot_access_chat(self):
        self.client.force_login(self.other_student)

        response = self.client.get(
            reverse(
                'chat_room',
                args=[self.course.id]
            )
        )

        self.assertEqual(response.status_code, 302)
