from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import StudentSignUpForm, InstructorSignUpForm, UserEditForm, StudentProfileForm, InstructorEditForm
from .models import Student, Instructor
from django.views.generic import TemplateView
from datetime import timedelta, date, datetime
from courses.models import Subject_Load, Subject_Offering, Subject_Load_List, DaySchedule
from appointments.models import ConsultationRequest
from collections import defaultdict
from courses.helper import get_current_academic_term
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()

def redirect_to_dashboard(request):
    return redirect('dashboard')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Student account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'There were errors in your form. Please correct them.')
    else:
        form = StudentSignUpForm()
    return render(request, 'student_signup.html', {'form': form})

def instructor_signup(request):
    if request.method == 'POST':
        form = InstructorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Instructor account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'There were errors in your form. Please correct them.')
    else:
        form = InstructorSignUpForm()
    return render(request, 'instructor_signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'student':
                    return redirect('student_dashboard')
                elif user.user_type == 'instructor':
                    return redirect('instructor_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def generate_time_blocks(start_time='08:00 AM', end_time='06:00 PM'):
    time_blocks = []
    start = datetime.strptime(start_time, '%I:%M %p')
    end = datetime.strptime(end_time, '%I:%M %p')

    current_time = start
    while current_time < end:
        next_time = current_time + timedelta(minutes=30)
        time_blocks.append(f"{current_time.strftime('%I:%M %p')} - {next_time.strftime('%I:%M %p')}")
        current_time = next_time

    return time_blocks

def time_in_block(event_time, time_block):
    # Parse the start and end times of the block
    block_start, block_end = time_block.split(" - ")
    block_start = datetime.strptime(block_start, "%I:%M %p")
    block_end = datetime.strptime(block_end, "%I:%M %p")

    # Parse the start and end times of the event
    event_start, event_end = event_time.split(" - ")
    event_start = datetime.strptime(event_start, "%I:%M %p")
    event_end = datetime.strptime(event_end, "%I:%M %p")
    
    # Check if the event is within the block time (either starting or ongoing)
    if (block_start <= event_end and event_start < block_end):
        return True
    else:
        return False

@login_required
def dashboard_view(request):
    current_year, current_semester = get_current_academic_term()
    
    today = date.today()

    # Initialize schedule data
    schedule_data = defaultdict(list)

    # Fetch class schedules
    if hasattr(request.user, 'student'):
        # Fetch approved subjects for students
        subject_load_list = Subject_Load_List.objects.filter(
            student=request.user.student,
            school_year=current_year,
            semester=current_semester,
            approval=True
        )
        enrolled_subjects = Subject_Load.objects.filter(
            subject_list__in=subject_load_list
        )
        class_schedules = DaySchedule.objects.filter(
            subject_offering__in=[enrollment.subject for enrollment in enrolled_subjects]
        )

        # Fetch student consultations
        consultations = ConsultationRequest.objects.filter(
            student=request.user.student,
            date__gte=today,
            approved=True
        )

    elif hasattr(request.user, 'instructor'):
        # Fetch instructor subjects
        instructor_subjects = Subject_Offering.objects.filter(
            instructor=request.user.instructor,
            academic_year=current_year,
            semester=current_semester
        )
        class_schedules = DaySchedule.objects.filter(
            subject_offering__in=instructor_subjects
        )
        # Fetch instructor consultations
        consultations = ConsultationRequest.objects.filter(
            instructor=request.user.instructor,
            date__gte=today,
            approved=True
        )
    else:
        class_schedules = []
        consultations = []

    # Organize class schedules by day
    for schedule in class_schedules:
        schedule_data[schedule.day.name].append({
            "time": f"{schedule.start_time.strftime('%I:%M %p')} - {schedule.end_time.strftime('%I:%M %p')}",
            "course": schedule.subject_offering.course.course_code,
            "location": schedule.subject_offering.room,
            "type": "class"
        })

    # Organize consultations by day
    for consultation in consultations:
        day_name = consultation.date.strftime('%A')  # Get day name from the date
        schedule_data[day_name].append({
            "time": f"{consultation.start_time.strftime('%I:%M %p')} - {consultation.end_time.strftime('%I:%M %p')}",
            "course": consultation.reason,
            "location": "Consultation Room",
            "type": "consultation"
        })
    processed_schedule = []
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    time_blocks = generate_time_blocks()

    for time_block in time_blocks:
        daily_events = []
        for day in days_of_week:
            events = []
            for event in schedule_data.get(day, []):
                if time_in_block(event['time'], time_block):
                    events.append(event)
            daily_events.append(events)
        processed_schedule.append({'time_block': time_block, 'events': daily_events})
    context = {
    "processed_schedule": processed_schedule,
    "days_of_week": days_of_week,
    }   
    return render(request, 'dashboard.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')

@login_required
def logout_view(request):
    messages.success(request, "You have been logged out successfully.")
    logout(request)
    return redirect('login')

class StudentProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = 'student_edit_profile.html'

    def get_object(self, queryset=None):
        # Ensure that only the logged-in student can edit their profile
        return Student.objects.get(user=self.request.user)

    def get_success_url(self):
        # Redirect to a success page (e.g., profile detail page)
        return reverse_lazy('dashboard')