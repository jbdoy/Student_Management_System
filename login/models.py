from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import time

class User(AbstractUser):
    class Meta:
        permissions = (("can_change_username", "Can change username"),)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentID = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Instructor(models.Model):
    instructor_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.instructor_id

class Course(models.Model):
    course_id = models.CharField(max_length=50, primary_key=True)
    course_name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    credit_hours = models.IntegerField()
    start_time = models.TimeField(default=time(9, 0)) 
    end_time = models.TimeField(default=time(10, 30)) 
    days_of_week = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_id})"

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    grade_value = models.CharField(max_length=50)
