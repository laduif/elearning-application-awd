from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import CourseForm, FeedbackForm, CourseMaterialForm
from .models import Course, Enrolment, Feedback, CourseMaterial, Notification, BlockStudent

## Must be logged in
@login_required
def create_course(request):
    if request.user.role != 'TEACHER':
        return redirect('home')

    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()

            return redirect('my_courses')

    else:
        form = CourseForm()

    return render(
        request,
        'courses/create_course.html',
        {'form': form}
    )

@login_required
def my_courses(request):
    if request.user.role != 'TEACHER':
        return redirect('home')

    courses = request.user.courses_taught.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'courses/my_courses.html',
        {'courses': courses}
    )

@login_required
def courses_list(request):
    courses = Course.objects.all().order_by('title')

    return render(
        request,
        'courses/courses_list.html',
        {'courses': courses}
    )

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id
    )

    is_enrolled = Enrolment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    has_feedback = Feedback.objects.filter(
        student=request.user,
        course=course
    ).exists()

    feedback = Feedback.objects.filter(course=course).select_related('student').order_by('-created_at')

    materials = CourseMaterial.objects.filter(course=course).order_by('-uploaded_at')

    return render(
        request,
        'courses/course_detail.html',
        {
            'course': course,
            'is_enrolled': is_enrolled,
            'has_feedback': has_feedback,
            'feedback': feedback,
            'materials': materials,
        }
    )

@login_required
def leave_feedback(request, course_id):
    if request.user.role != 'STUDENT':
        return redirect('course_detail', course_id=course_id)

    course = get_object_or_404(Course, id=course_id)

    is_enrolled = Enrolment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    if not is_enrolled:
        return redirect(
            'course_detail',
            course_id=course.id
        )

    existing_feedback = Feedback.objects.filter(
        student=request.user,
        course=course
    ).first()

    if existing_feedback:
        return redirect(
            'course_detail',
            course_id=course.id
        )

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.course = course
            feedback.save()

            return redirect('course_detail', course_id=course.id)

    else:
        form = FeedbackForm()

    return render(
        request, 'courses/leave_feedback.html', {'course': course, 'form': form,}
    )

@login_required
def enrol_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'STUDENT':
        return redirect('course_detail', course_id=course.id)

    blocked = BlockStudent.objects.filter(
        teacher=course.teacher,
        student=request.user,
        course=course
    ).exists()

    if blocked:
        return redirect('course_detail', course_id=course.id)

    if request.method == 'POST':
        enrolment, created = Enrolment.objects.get_or_create(
            student=request.user,
            course=course
        )

        if created:
            Notification.objects.create(
                user=course.teacher,
                message=(f'{request.user.username} has enrolled '
                         f'on your course "{course.title}".')
            )

    return redirect('course_detail', course_id=course.id)

@login_required
def my_enrolments(request):
    if request.user.role != 'STUDENT':
        return redirect('home')

    enrolments = request.user.enrolments.select_related(
        'course',
        'course__teacher'
    ).order_by('-enrolled_at')

    return render(
        request,
        'courses/my_enrolments.html',
        {'enrolments': enrolments}
    )

@login_required
def course_students(request, course_id):
    if request.user.role != 'TEACHER':
        return redirect('home')

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrolments = course.enrolments.select_related('student').order_by('student__username')

    return render(
        request,
        'courses/course_students.html',
        {
            'course': course,
            'enrolments': enrolments,
        }
    )


@login_required
def add_material(request, course_id):
    if request.user.role != 'TEACHER':
        return redirect('home')

    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)

        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()

            enrolments = Enrolment.objects.filter(course=course).select_related('student')

            for enrolment in enrolments:
                Notification.objects.create(
                    user=enrolment.student,
                    message=(
                        f'New material "{material.title}" has been '
                        f'added to your course "{course.title}".')
                )

            return redirect(
                'course_detail',
                course_id=course.id
            )

    else:
        form = CourseMaterialForm()

    return render(request, 'courses/add_material.html', {'course': course, 'form': form,})

@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-created_at')

    return render(
        request,
        'courses/notifications.html',
        {
            'notifications': user_notifications,
        }
    )

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect('notifications')


@login_required
def remove_student(request, course_id, student_id):
    if request.user.role != 'TEACHER':
        return redirect('home')

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrolment = get_object_or_404(
        Enrolment,
        course=course,
        student_id=student_id
    )

    enrolment.delete()

    return redirect(
        'course_students',
        course_id=course.id
    )


@login_required
def block_student(request, course_id, student_id):
    if request.user.role != 'TEACHER':
        return redirect('home')

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrolment = get_object_or_404(
        Enrolment,
        course=course,
        student_id=student_id
    )

    BlockStudent.objects.get_or_create(
        teacher=request.user,
        student_id=student_id,
        course=course
    )

    enrolment.delete()

    return redirect(
        'course_students',
        course_id=course.id
    )