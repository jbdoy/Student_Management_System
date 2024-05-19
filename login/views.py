from django.shortcuts import render, redirect, get_object_or_404    
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from django.http import HttpResponse, JsonResponse
from .models import User
from .models import Student
from .models import Instructor
from .models import Course
from .models import Enrollment
from .models import Grade
from django.contrib.auth import logout
from django.db import IntegrityError
from .forms import StudentForm
from .forms import AddCourseForm


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)
            return render(request, 'login_page/home.html')
        else:
            return render(request, 'login_page/login_form.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login_page/login_form.html')
       
def register_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            login(request, user)
            return redirect('login_form') 

        except IntegrityError:
            return render(request, 'login_page/register_form.html', {'error': 'This username is already taken. Please choose a different one.'})

    else:
        return render(request, 'login_page/register_form.html')

@login_required
def home_page(request):
    
    courses = Course.objects.all()  
    return render(request, 'login_page/home.html', {'courses': courses})

def view_students(request):
    return render(request, 'login_page/view_students.html')
def enroll_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        return redirect('enrolled_courses_page')  
    else:
        
        course = get_object_or_404(Course, pk=course_id)
        return render(request, 'login_page/view_courses.html', {'course': course})
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('view_courses')  
    else:
        form = CourseForm(instance=course)
    return render(request, 'login_page/edit_course.html', {'form': form, 'course': course})

@require_POST
def delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    course.delete()
    return redirect(reverse('home'))

class CourseUpdateView(UpdateView):
    model = Course
    form_class = AddCourseForm
    template_name = 'edit_course.html' 
    success_url = reverse_lazy('home')  

    def get_object(self):
        course_id = self.kwargs.get("course_id")
        return get_object_or_404(Course, course_id=course_id)

def view_instructors(request):
    all_instructors = Instructor.objects.all
    return render(request, 'login_page/view_instructors.html', {'all':all_instructors})
def view_enrollments(request):
    
    student = Student.objects.get(user=request.user)
    
    enrollments = Enrollment.objects.filter(student_id=student)
    
    return render(request, 'login_page/view_enrollments.html', {'enrollments': enrollments})


def enroll_course(request):
    courses = Course.objects.all()  
    return render(request, 'login_page/enroll_course.html', {'courses': courses})
def add_instructors(request):
    if request.method == 'POST':
        instructor_id = request.POST['instructor_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
       
        if Instructor.objects.filter(instructor_id=instructor_id).exists():
           
            return render(request, 'login_page/add_instructors.html', {'error': True})
            
        
        new_instructor = Instructor(
            instructor_id=instructor_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        
     
        new_instructor.save()
       
        return redirect('view_instructors')
    else:
        return render(request, 'login_page/add_instructors.html', {'error': False})

def edit_instructor(request, instructor_id):
    
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)

    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        
        instructor.first_name = first_name
        instructor.last_name = last_name
        instructor.email = email
        instructor.phone_number = phone_number

        
        instructor.save()

        
        return redirect('view_instructors')
    else:
        
        return render(request, 'login_page/edit_instructor.html', {'instructor': instructor})

def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)
    if request.method == 'POST':
        instructor.delete()
        return redirect('view_instructors')
    return render(request, 'login_page/view_instructors.html', {'instructor': instructor})

def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_added_success')
    else:
        form = AddCourseForm()
    return render(request, 'login_page/add_course.html', {'form': form})
def course_added_success(request):
    
    return render(request, 'login_page/course_added_success.html')

def student_view_course(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'login_page/student_view_course.html', context)
    
def student_view_grades(request):
    # Retrieve the current student (user)
    student = request.user.student  # Assuming you have a related Student model for User

    # Retrieve grades for the current student through the Enrollment model
    grades = Grade.objects.filter(enrollment__student_id=student).values('enrollment__course_id', 'grade_value')

    return render(request, 'login_page/student_view_grades.html', {'grades': grades})

def student_view_profile(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url') 
    else:
        form = StudentForm()
    return render(request, 'login_page/student_view_profile.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        admin_username = request.POST['admin_username']
        admin_password = request.POST['admin_password']

        admin_user = authenticate(request, username=admin_username, password=admin_password, is_admin=True)

        if admin_user is not None:
            login(request, admin_user)
            return render(request, 'login_page/admin_home.html')
        else:
            return render(request, 'login_page/admin_login.html', {'admin_error': 'Invalid admin credentials'})
    else:
        return render(request, 'login_page/admin_login.html')

def edit_student_profile(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = Student(user=user)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('login_page/student_view_profile')
        else:
            messages.error(request, 'Error updating profile. Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'login_page/student_edit_profile.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('login_form')

