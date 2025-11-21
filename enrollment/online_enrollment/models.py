from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=150, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    student_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    course = models.CharField(max_length=150, blank=True)
    year = models.CharField(max_length=50, blank=True)
    section = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or self.user.username} ({self.student_id or 'no-id'})"


class Subject(models.Model):
    subject_code = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    instruction = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    time = models.TimeField()

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"
