from django.urls import path
from . import views

urlpatterns = [
    # Course-related views
    path('', views.CourseListView.as_view(), name='course_list'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # Subject offerings related views
    path('my_subjects/', views.UserCoursesListView.as_view(), name='my_subjects'),
    path('offerings/', views.SubjectOfferingListView.as_view(), name='subject_offering_list'),
    path('offerings/create/', views.SubjectOfferingCreateView.as_view(), name='subject_offering_create'),
    path('offerings/<int:pk>/update/', views.SubjectOfferingUpdateView.as_view(), name='subject_offering_update'),
    path('offerings/<int:pk>/delete/', views.SubjectOfferingDeleteView.as_view(), name='subject_offering_delete'),

    path('my_students/', views.SelectStudentView.as_view(), name='select_student'),
    path('enroll_student/<str:student_id>/', views.ManageSubjectLoadView.as_view(), name='manage_subject_load'),
    path('search_courses/', views.search_courses, name='search_courses'),
    path('enroll_course/', views.enroll_course, name='enroll_course'),
    path('unenroll_course/', views.unenroll_course, name='unenroll_course'),
    path('finalize_enrollment/<int:subject_load_list_id>/', views.FinalizeEnrollmentView.as_view(), name='finalize_enrollment'),
    path('enrollment_summary/<int:subject_load_list_id>/', views.EnrollmentSummaryView.as_view(), name='enrollment_summary'),
    #path('generate-registration-form/<int:subject_load_list_id>/', views.generate_registration_form, name='generate_registration_form'),
    path('generate-registration-form/<int:subject_load_list_id>/', views.generate_registration_forms_pdf, name='generate_registration_form'),
]
