from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .decoratos import *
from .forms import *


def index(request):
    courses = Course.objects.all()
    students = Student.objects.all()

    paginator = Paginator(students, 3)
    page = request.GET.get('page', 1)

    context = {
        'courses': courses,
        'students': paginator.get_page(page),
        'current_year': datetime.now().year
    }

    return render(request, 'index.html', context)


@login_required
def search(request: WSGIRequest):
    query = request.GET.get('q')
    if query:
        results = Course.objects.filter(title__icontains=query)

        context = {
            'query': query,
            'results': results
        }

        return render(request, 'search.html', context)
    return redirect('index')


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = Student.objects.filter(course_id=course_id)

    paginator = Paginator(students, 3)
    page = request.GET.get('page', 1)

    context = {
        'courses': [course],
        'students': paginator.get_page(page),
        'current_year': datetime.now().year
    }

    return render(request, 'index.html', context)


@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    context = {
        'student': student,
        'current_year': datetime.now().year
    }

    return render(request, 'student.html', context)


@permission_required('manager.add_course', login_url='not_found')
def addCourse(request: WSGIRequest):
    if request.method == 'POST':
        form = CourseForm(data=request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Ma'lumot muvaffaqiyatli qo'shildi!")
            return redirect('index')
    else:
        form = CourseForm()

    context = {
        'forms': form,
        'current_year': datetime.now().year
    }

    return render(request, 'addCourse.html', context)


@permission_required('manager.change_course', login_url='not_found')
def updateCourse(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = CourseForm(data=request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi!")
            return redirect('course_detail', course_id=course_id)

    else:
        form = CourseForm(instance=course)

    context = {
        'forms': form,
        'current_year': datetime.now().year
    }

    return render(request, 'addCourse.html', context)


@permission_required('manager.delete_course', login_url='not_found')
def deleteCourse(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()

    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi!")
    return redirect('index')


def register(request: WSGIRequest):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz va tizimga kirish uchun tayyorsiz.")
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'forms': form,
        'current_year': datetime.now().year
    }

    return render(request, 'auth/register.html', context)


def loginView(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request,
                             "Hisobingizga muvaffaqiyatli kirdingiz. Endi barcha imkoniyatlardan foydalana olasiz.")
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'forms': form
    }

    return render(request, 'auth/login.html', context)


@login_required
def logoutView(request: WSGIRequest):
    logout(request)

    messages.success(request, "Tizimdan chiqish muvaffaqiyatli amalga oshirildi.")
    return redirect('login')


@staff_required(login_url='not_found')
def sendEmail(request: WSGIRequest):
    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            users = MyUser.objects.all()
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            for user in users:
                send_mail(
                    subject,
                    message,
                    None,
                    [user.email],
                    fail_silently=False
                )

            messages.success(request, "Xabaringiz foydalanuvchilarga muvaffaiyatli yuborildi.")
            return redirect('send_email')
    else:
        form = EmailForm()

    context = {
        'form': form,
        'current_year': datetime.now().year
    }

    return render(request, 'sendEmail.html', context)


@login_required
def settings(request):
    user = get_object_or_404(MyUser, username=request.user.username)
    form = SettingsForm(instance=user)
    password_form = PasswordForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = SettingsForm(data=request.POST, files=request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Ma'lumotlar muvaffaqiyatli saqlandi.")
                return redirect('personal_data')

        elif 'change_password' in request.POST:
            password_form = PasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():

                password_form.save()
                update_session_auth_hash(request, password_form.user)

                messages.success(request, "Parol muvaffaqiyatli o'zgartirildi.")
                return redirect('change_password')
        elif 'delete_photo' in request.POST:
            if user.photo:
                user.photo = None
                user.save()

                messages.success(request, "Profil rasmingiz o'chirildi.")
            else:
                messages.error(request, "Sizda profil rasm mavjud emas!")

            return redirect('delete_photo')

        elif 'delete_account' in request.POST:
            user.delete()

            messages.success(request, "Hisobingiz muvaffaqiyatli o'chirildi.")
            return redirect('index')


    context = {
        'forms': form,
        'changePassword': password_form,
        'current_year': datetime.now().year
    }

    return render(request, 'settings.html', context)

def not_found(request):
    context = {
        'current_year': datetime.now().year
    }

    return render(request, '404.html', context)
