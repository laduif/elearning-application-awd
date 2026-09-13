from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import BlockStudent, Course, Enrolment


@login_required
def chat_room(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user == course.teacher:
        allowed = True
    else:
        allowed = Enrolment.objects.filter(
            course=course,
            student=request.user
        ).exists()

        blocked = BlockStudent.objects.filter(
            teacher=course.teacher,
            student=request.user,
            course=course
        ).exists()

        if blocked:
            allowed = False

    if not allowed:
        return redirect('course_detail', course_id=course.id)

    return render(
        request,
        'chat/chat.html',
        {
            'course': course,
        }
    )