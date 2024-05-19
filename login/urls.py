from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_form, name='login_form'),
    path('register_form', views.register_form, name='register_form'),
    path('view/students/', views.view_students, name='view_students'),
    path('view/courses/', views.student_view_course, name='student_view_course'),
    path('view/instructors/', views.view_instructors, name='view_instructors'),
]
