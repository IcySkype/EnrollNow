from django.contrib import admin
from .models import Student, Instructor, User

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(User)