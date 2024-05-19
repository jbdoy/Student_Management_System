from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Student
from .models import Instructor
from .models import Course
from .models import Enrollment
from .models import Grade

admin.site.register(User, UserAdmin)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Grade)