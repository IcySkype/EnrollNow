from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ConsultationRequest
from .forms import ConsultationRequestForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now

class ConsultationRequestListView(LoginRequiredMixin, ListView):
    model = ConsultationRequest
    template_name = "list.html"
    context_object_name = "consultation_requests"

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return ConsultationRequest.objects.filter(student__user=user)
        elif user.user_type == 'instructor':
            return ConsultationRequest.objects.filter(instructor__user=user)
        return ConsultationRequest.objects.none()
    
class ConsultationRequestCreateView(LoginRequiredMixin, CreateView):
    model = ConsultationRequest
    form_class = ConsultationRequestForm
    template_name = "create.html"
    success_url = reverse_lazy("appointment_list")

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current logged-in user
        return kwargs
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'student':
            return redirect("appointment_list")
        return super().dispatch(request, *args, **kwargs)
    
class ConsultationRequestDetailView(LoginRequiredMixin, DetailView):
    model = ConsultationRequest
    template_name = "detail.html"
    context_object_name = "consultation_request"

@login_required
def approve_consultation_request(request, pk):
    # Get the consultation request
    consultation_request = get_object_or_404(ConsultationRequest, pk=pk)

    # Ensure the logged-in user is the instructor for this request
    if request.user.user_type != 'instructor' or consultation_request.instructor.user != request.user:
        return HttpResponseForbidden("You are not authorized to approve this request.")

    # Approve the consultation request
    consultation_request.approve()
    return redirect("appointment_list")