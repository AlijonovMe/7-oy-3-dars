from django.contrib import admin
from .models import *


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')
    list_display_links = ('id', 'username')
    list_filter = ('id', 'username')
    list_per_page = 10
    search_fields = ('id', 'username')
    actions_on_top = False
    actions_on_bottom = True


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('id', 'title')
    list_per_page = 10
    search_fields = ('id', 'title')
    actions_on_top = False
    actions_on_bottom = True


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'email', 'enrolled_at', 'course')
    list_display_links = ('name', 'lastname')
    list_filter = ('id', 'name')
    list_per_page = 10
    search_fields = ('id', 'name')
    actions_on_top = False
    actions_on_bottom = True


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
