from django import forms
from .models import Student
from .models import User
from .models import Course
from django.contrib.auth.models import AbstractUser

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'dateofbirth', 'address', 'phonenumber', 'email',]
class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'instructor', 'credit_hours', 'start_time', 'end_time', 'days_of_week']



