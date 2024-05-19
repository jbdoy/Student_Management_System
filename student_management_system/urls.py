from django.contrib import admin
from django.urls import path, include

from login.views import login_form, logout_view, register_form, home_page, admin_login, student_view_course, student_view_grades, student_view_profile, edit_student_profile,view_students,view_instructors,edit_instructor,delete_instructor, add_instructors, add_course, edit_course, delete_course, enroll_course, course_added_success

urlpatterns = [
    path('login/', login_form, name='login_form'), 
    path('logout/', logout_view, name='logout'), 
    path('register/', register_form, name='register_form'),
    path('admin/login', admin_login, name='admin_login'),
    path('home/', home_page, name='home'),
    path('view/students/', view_students, name='view_students'),
    path('view/instructors/',view_instructors, name='view_instructors'),
    path('edit/instructor/', edit_instructor, name='edit_instructor'),
    path('view/instructors/',delete_instructor, name='delete_instructor'),
    path('add/instructor/', add_instructors, name='add_instructor'),
    path('add/course/', add_course, name='add_course'),
    path('add/course/success/', course_added_success, name='course_added_success'),
    path('enroll_course/', enroll_course, name='enroll_course'),
    path('edit/course/', edit_course, name='edit_course'),
    path('course/delete/<str:course_id>/', delete_course, name='delete_course'),
    path('student/view_course/', student_view_course, name='student_view_course'),
    path('student/view_grades/', student_view_grades, name='student_view_grades'),
    path('student/view_profile/', student_view_profile, name='student_view_profile'),
    path('student/edit_profile/', edit_student_profile, name='student_edit_profile'),
    path('', include("login.urls")),
    path("admin/", admin.site.urls),
]


