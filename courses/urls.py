from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/course/create/', views.create_course, name='create_course'),
    path('instructor/course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('instructor/course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('instructor/course/<int:course_id>/upload/', views.upload_lesson, name='upload_lesson'),
]
