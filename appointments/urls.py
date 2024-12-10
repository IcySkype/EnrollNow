from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ConsultationRequestListView.as_view(), name='appointment_list'),
    path("create/", views.ConsultationRequestCreateView.as_view(), name="appointment_create"),
    path("<int:pk>/", views.ConsultationRequestDetailView.as_view(), name="appointment_detail"),
    path("<int:pk>/approve/", views.approve_consultation_request, name="appointment_approve"),
]