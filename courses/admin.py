from django.contrib import admin

from .models import Course, Enrolment, Feedback, CourseMaterial, Notification, BlockStudent

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    search_fields = ('student__username', 'course__title')
    list_filter = ('enrolled_at',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating', 'created_at')
    search_fields = ('student__username', 'course__title', 'comment')
    list_filter = ('rating', 'created_at')

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_at')
    search_fields = ('title', 'course__title')
    list_filter = ('uploaded_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','message','is_read','created_at')
    search_fields = ('user__username','message')
    list_filter = ('is_read','created_at')

@admin.register(BlockStudent)
class BlockStudentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'course', 'blocked_at')
    search_fields = ('teacher__username', 'student__username', 'course__title')
    list_filter = ('blocked_at',)