from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField()

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_taught'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Enrolment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrolments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrolments'
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_enrolment'
            )
        ]

    def __str__(self):
        return f'{self.student.username} - {self.course.title}'


class Feedback(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_feedback'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_feedback'
            )
        ]

    def __str__(self):
        return f'{self.student.username} - {self.course.title}'


class CourseMaterial(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    title = models.CharField(max_length=200)

    file = models.FileField(upload_to='course_materials')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.message}'


class BlockStudent(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_students'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by_teacher'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='blocked_students'
    )

    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'student', 'course'],
                name='unique_blocked_student_course')
        ]

    def __str__(self):
        return (
            f'{self.student.username} block from '
            f'{self.course.title}'
        )