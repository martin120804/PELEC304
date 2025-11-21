from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, StudentForm
from django.contrib.auth.decorators import login_required
from .models import Student, Subject
from django.db import transaction
from django.contrib.auth.models import User


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=True)
                # create empty student profile for this user
                Student.objects.create(user=user, name=user.username)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login_user')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'online_enrollment/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # go to student profile after login
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid input.')
    else:
        form = AuthenticationForm()

    return render(request, 'online_enrollment/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login_user')


@login_required(login_url='login_user')
def home(request):
    # kept for backward compatibility; could redirect to profile as well
    return render(request, 'online_enrollment/home.html')


@login_required(login_url='login_user')
def profile(request):
    user_id = request.GET.get('u')
    if user_id and request.user.is_staff:
        # staff can view any student's profile
        target_user = get_object_or_404(User, id=user_id)
    else:
        target_user = request.user

    student, created = Student.objects.get_or_create(user=target_user, defaults={'name': target_user.username})
    return render(request, 'online_enrollment/profile.html', {'student': student})



@login_required(login_url='login_user')
def edit_profile(request):
    student, created = Student.objects.get_or_create(user=request.user, defaults={'name': request.user.username})
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the form errors below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'online_enrollment/edit_profile.html', {'form': form})

@login_required(login_url='login_user')
def dashboard(request):
    """
    Dashboard visible to all logged-in users.
    Shows all students and all subjects.
    """
    students = Student.objects.select_related('user').all().order_by('name')
    subjects = Subject.objects.all().order_by('subject_code')
    return render(request, 'online_enrollment/dashboard.html', {
        'students': students,
        'subjects': subjects,
    })