from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    photo = models.ImageField(upload_to='users/photo', null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['id']


class Course(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="Nomi")
    description = models.TextField(default="Ma'lumot qo'shilmadi.", verbose_name="Tavsifi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return self.title

    class Meta:
        # unique_together = ('title',)
        verbose_name = "Kurs "
        verbose_name_plural = "Kurslar"
        ordering = ['id']


class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name="Ismi")
    lastname = models.CharField(max_length=50, verbose_name="Familiyasi")
    email = models.EmailField(max_length=100, verbose_name="Elektron pochta manzili")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.lastname}"

    class Meta:
        verbose_name = "Talaba "
        verbose_name_plural = "Talabalar"
        ordering = ['id']