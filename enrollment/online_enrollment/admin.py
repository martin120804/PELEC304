from django.contrib import admin
from .models import Student, Subject

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'user', 'course', 'year', 'section')
    search_fields = ('name', 'student_id', 'user__username', 'course')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'instruction', 'room', 'department', 'time')
    search_fields = ('subject_code', 'subject_name', 'department')
