from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'student_id', 'course', 'year', 'section']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'student_id': forms.TextInput(attrs={'placeholder': 'e.g. 2025-0001'}),
            'course': forms.TextInput(),
            'year': forms.TextInput(),
            'section': forms.TextInput(),
            'age': forms.NumberInput(),
        }
