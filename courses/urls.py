from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.courses_list,
        name='courses_list',
    ),

    path(
        'notifications/',
        views.notifications,
        name='notifications',
    ),

    path(
        'notifications/<int:notification_id>/read/',
        views.mark_notification_read,
        name='mark_notification_read',
    ),

    path(
        'create/',
        views.create_course,
        name='create_course',
    ),

    path(
        'my-courses/',
        views.my_courses,
        name='my_courses',
    ),

    path(
        'my-enrolments/',
        views.my_enrolments,
        name='my_enrolments',
    ),

    path(
        '<int:course_id>/enrol/',
        views.enrol_course,
        name='enrol_course',
    ),

    path(
        '<int:course_id>/students/',
        views.course_students,
        name='course_students',
    ),

    path(
        '<int:course_id>/students/<int:student_id>/remove/',
        views.remove_student,
        name='remove_student',
    ),

    path(
        '<int:course_id>/students/<int:student_id>/block/',
        views.block_student,
        name='block_student',
    ),

    path(
        '<int:course_id>/feedback/',
        views.leave_feedback,
        name='leave_feedback',
    ),

    path(
        '<int:course_id>/materials/add/',
        views.add_material,
        name='add_material',
    ),

    path(
        '<int:course_id>/',
        views.course_detail,
        name='course_detail',
    ),
]