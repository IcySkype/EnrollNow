from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.redirect_to_dashboard),
    path('student_signup/', views.student_signup, name='student_signup'),
    path('instructor_signup/', views.instructor_signup, name='instructor_signup'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    path('student/profile/edit/', views.StudentProfileUpdateView.as_view(), name='student_profile_edit'),
]