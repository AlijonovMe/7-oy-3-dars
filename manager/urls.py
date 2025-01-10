from django.urls import path
from .views import *

urlpatterns = [
    # home
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('send-email/', sendEmail, name='send_email'),

    # course
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/update/', updateCourse, name='updateCourse'),
    path('course/<int:course_id>/delete/', deleteCourse, name='deleteCourse'),
    path('course/add/', addCourse, name='addCourse'),

    # student
    path('student/<int:student_id>/', student_detail, name='student_detail'),

    # auth
    path('auth/register/', register, name='register'),
    path('auth/login/', loginView, name='login'),
    path('auth/logout/', logoutView, name='logout'),

    # not found
    path('not-found/', not_found, name='not_found'),

    # settings
    path('settings/', settings, name='settings'),
    path('settings/personal-data/update/', settings, name='personal_data'),
    path('settings/personal-data/photo/delete', settings, name='delete_photo'),
    path('settings/password/change/', settings, name='change_password'),
]
