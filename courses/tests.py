from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import (
    BlockStudent,
    Course,
    CourseMaterial,
    Enrolment,
    Feedback,
    Notification,
)


class CourseTests(TestCase):

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

        self.course = Course.objects.create(
            title='Web Development',
            description='A test course.',
            teacher=self.teacher
        )

    def test_teacher_can_create_course(self):
        self.client.force_login(self.teacher)

        response = self.client.post(
            reverse('create_course'),
            {
                'title': 'Python Programming',
                'description': 'Learn Python.'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Course.objects.filter(
                title='Python Programming',
                teacher=self.teacher
            ).exists()
        )

    def test_student_can_enrol_on_course(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse(
                'enrol_course',
                args=[self.course.id]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Enrolment.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    def test_teacher_receives_enrolment_notification(self):
        self.client.force_login(self.student)

        self.client.post(
            reverse(
                'enrol_course',
                args=[self.course.id]
            )
        )

        self.assertTrue(
            Notification.objects.filter(
                user=self.teacher
            ).exists()
        )

    def test_blocked_student_cannot_enrol(self):
        BlockStudent.objects.create(
            teacher=self.teacher,
            student=self.student,
            course=self.course
        )

        self.client.force_login(self.student)

        self.client.post(
            reverse(
                'enrol_course',
                args=[self.course.id]
            )
        )

        self.assertFalse(
            Enrolment.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    def test_enrolled_student_can_leave_feedback(self):
        Enrolment.objects.create(
            student=self.student,
            course=self.course
        )

        self.client.force_login(self.student)

        response = self.client.post(
            reverse(
                'leave_feedback',
                args=[self.course.id]
            ),
            {
                'rating': 5,
                'comment': 'Excellent course.'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Feedback.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    def test_non_enrolled_student_cant_leave_feedback(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse(
                'leave_feedback',
                args=[self.course.id]
            ),
            {
                'rating': 5,
                'comment': 'I should not be able to post this.'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Feedback.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    def test_teacher_can_remove_student(self):
        Enrolment.objects.create(
            student=self.student,
            course=self.course
        )

        self.client.force_login(self.teacher)

        self.client.get(
            reverse(
                'remove_student',
                args=[
                    self.course.id,
                    self.student.id
                ]
            )
        )

        self.assertFalse(
            Enrolment.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    def test_teacher_can_block_student(self):
        Enrolment.objects.create(
            student=self.student,
            course=self.course
        )

        self.client.force_login(self.teacher)

        self.client.get(
            reverse(
                'block_student',
                args=[
                    self.course.id,
                    self.student.id
                ]
            )
        )

        self.assertTrue(
            BlockStudent.objects.filter(
                teacher=self.teacher,
                student=self.student,
                course=self.course
            ).exists()
        )

        self.assertFalse(
            Enrolment.objects.filter(
                student=self.student,
                course=self.course
            ).exists()
        )

    def test_teacher_can_upload_course_material(self):
        self.client.force_login(self.teacher)

        test_file = SimpleUploadedFile(
            'lesson.txt',
            b'This is test course material.',
            content_type='text/plain'
        )

        response = self.client.post(
            reverse(
                'add_material',
                args=[self.course.id]
            ),
            {
                'title': 'Lesson One',
                'file': test_file
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            CourseMaterial.objects.filter(
                course=self.course,
                title='Lesson One'
            ).exists()
        )
