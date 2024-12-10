from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import  JsonResponse, HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from django.contrib.staticfiles import finders
import pdfkit
from .models import Course, Subject_Offering, Subject_Load, Subject_Load_List, DaySchedule
from user.models import Student, Instructor
from .forms import SubjectOfferingForm, CourseForm, DayScheduleFormSet, CourseSearchForm
from .decorators import department_head_required
from .helper import get_current_academic_term
from django.template import Template, Context
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

#COURSE CRUD--------------------------------------------------
class CourseListView(ListView):
    model = Course
    template_name = 'course_list2.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(course_code__icontains=query) |
                Q(desc__icontains=query) |
                Q(prereq__course_code__icontains=query)
            )
        return queryset
    
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    template_name = 'course_form.html'

    @method_decorator(department_head_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    template_name = 'course_form.html'

    @method_decorator(department_head_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')
    template_name = 'course_confirm_delete.html'

    @method_decorator(department_head_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#SUBJECT OFFERING CRUD---------------------------------------------------------------------
class UserCoursesListView(ListView):
    model = Subject_Offering
    template_name = 'subject_offering_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_academic_year, current_semester = get_current_academic_term()
        context['current_academic_year'] = current_academic_year
        context['current_semester'] = current_semester
        user = self.request.user
        if user.user_type == 'student':
            student = user.student
            context['is_student'] = True
            subject_load_list = Subject_Load_List.objects.get(
                    student=student,
                    school_year=current_academic_year,
                    semester=current_semester,
                    approval=True
                )
            context['enrolled_subjects'] = Subject_Load.objects.filter(subject_list_id=subject_load_list.id)
        elif user.user_type == 'instructor':
            instructor = user.instructor
            context['is_instructor'] = True
            context['handled_subjects'] = Subject_Offering.objects.filter(instructor=instructor, 
                                                                          academic_year=current_academic_year, 
                                                                          semester=current_semester)
        
        # Adding course descriptions and schedules
        subject_offerings = context['object_list']
        
        for offering in subject_offerings:
            # Add course description
            offering.course_description = offering.course.desc if offering.course.desc else "No description available"
            
            # Add schedule (days and time slots)
            offering.schedule = []
            
            # Sorting the day schedules by day (if necessary) for ordered output
            day_schedules = offering.day_schedules.all().order_by('day__id', 'start_time')

            # Format the schedule string: "Mon 10:30am-12:00pm; Wed 1:00pm-2:30pm"
            for schedule in day_schedules:
                day_short_name = schedule.day.name[:3]  # Get the first 3 letters of the day
                time_slot = f"{schedule.start_time.strftime('%I:%M%p').lower()}-{schedule.end_time.strftime('%I:%M%p').lower()}"
                offering.schedule.append(f"{day_short_name} {time_slot}")

            # Join all the days and time slots with a semicolon
            offering.schedule = "; ".join(offering.schedule)

        return context

class SubjectOfferingListView(ListView):
    model = Subject_Offering
    template_name = 'subject_offering_list2.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get current academic term
        current_academic_year, current_semester = get_current_academic_term()
        
        # Filter by academic period
        queryset = queryset.filter(
            Q(academic_year=current_academic_year) &
            Q(semester=current_semester)
        )
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(course__course_code__icontains=query)|
                Q(offer_code__icontains=query)
            )

        # Prefetch related DaySchedule to access 'day' and other details
        queryset = queryset.prefetch_related('day_schedules__day')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_academic_year, current_semester = get_current_academic_term()
        context['current_academic_year'] = current_academic_year
        context['current_semester'] = current_semester
        user = self.request.user
        if user.user_type == 'student':
            student = user.student
            context['is_student'] = True
            subject_load_list = Subject_Load_List.objects.get(
                    student=student,
                    school_year=current_academic_year,
                    semester=current_semester
                )
            context['enrolled_subjects'] = Subject_Load.objects.filter(subject_list_id=subject_load_list.id)
        elif user.user_type == 'instructor':
            context['is_instructor'] = True
        
        # Adding course descriptions and schedules
        subject_offerings = context['object_list']
        
        for offering in subject_offerings:
            # Add course description
            offering.course_description = offering.course.desc if offering.course.desc else "No description available"
            
            # Add schedule (days and time slots)
            offering.schedule = []
            
            # Sorting the day schedules by day (if necessary) for ordered output
            day_schedules = offering.day_schedules.all().order_by('day__id', 'start_time')

            # Format the schedule string: "Mon 10:30am-12:00pm; Wed 1:00pm-2:30pm"
            for schedule in day_schedules:
                day_short_name = schedule.day.name[:3]  # Get the first 3 letters of the day
                time_slot = f"{schedule.start_time.strftime('%I:%M%p').lower()}-{schedule.end_time.strftime('%I:%M%p').lower()}"
                offering.schedule.append(f"{day_short_name} {time_slot}")

            # Join all the days and time slots with a semicolon
            offering.schedule = "; ".join(offering.schedule)
            

        return context

class SubjectOfferingCreateView(CreateView):
    model = Subject_Offering
    form_class = SubjectOfferingForm
    template_name = 'subject_offering_form.html'
    success_url = reverse_lazy('subject_offering_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DayScheduleFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DayScheduleFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()  # Save the Subject Offering instance first

        # Prepare the post data for the formset
        post_data = self.request.POST.copy()
        selected_days = post_data.getlist('days')  # Get selected days

        # Prepare formset data from the POST data
        post_data['day_schedule-TOTAL_FORMS'] = str(len(selected_days))
        post_data['day_schedule-INITIAL_FORMS'] = '0'
        post_data['day_schedule-MIN_NUM_FORMS'] = '0'
        post_data['day_schedule-MAX_NUM_FORMS'] = '7'

        # Map the dynamic fields like start_time_X and end_time_X to the formset format
        for idx, day in enumerate(selected_days):
            post_data[f'day_schedule-{idx}-day'] = day
            post_data[f'day_schedule-{idx}-start_time'] = post_data.get(f'start_time_{day}')
            post_data[f'day_schedule-{idx}-end_time'] = post_data.get(f'end_time_{day}')

        # Now initialize the formset with the updated post_data
        formset = DayScheduleFormSet(post_data, instance=self.object, prefix='day_schedule')

        if formset.is_valid():
            formset.save()  # Save valid formset data
        else:
            return self.form_invalid(form)

        # Remove schedules for unselected days
        selected_days = form.cleaned_data['days']
        self.object.day_schedules.exclude(day__in=selected_days).delete()

        return redirect(self.success_url)
    
    def form_invalid(self, form):
        formset = DayScheduleFormSet(self.request.POST, instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
    
    def get_success_url(self):
        return reverse_lazy('subject_offering_list')  # Redirect back to subject offering list

    @method_decorator(department_head_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class SubjectOfferingUpdateView(UpdateView):
    model = Subject_Offering
    form_class = SubjectOfferingForm
    template_name = 'subject_offering_form.html'
    success_url = reverse_lazy('subject_offering_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DayScheduleFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DayScheduleFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('subject_offering_list')  # Redirect back to subject offering list

    @method_decorator(department_head_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class SubjectOfferingDeleteView(DeleteView):
    model = Subject_Offering
    success_url = reverse_lazy('subject_offering_list')
    template_name = 'subject_offering_confirm_delete.html'

    @method_decorator(department_head_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#ENROLLMENT/SUBJECT LOAD LIST CRUD-----------------------------------------------------
class SelectStudentView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        # Get the instructor's department and match with students
        instructor = self.request.user.instructor
        students = Student.objects.filter(user__department=instructor.user.department)

        # Get current year and semester for enrollment check
        current_year, current_semester = get_current_academic_term()

        # Assign student enrollment status
        for student in students:
            try:
                subject_load_list = Subject_Load_List.objects.get(
                    student=student,
                    school_year=current_year,
                    semester=current_semester
                )
                # Check if the enrollment is approved or pending
                if subject_load_list.approval:
                    student.enrollment_status = 'approved'
                else:
                    student.enrollment_status = 'pending'

            except Subject_Load_List.DoesNotExist:
                student.enrollment_status = 'unenrolled'

        return students
    
#add subjects for enrollment
class ManageSubjectLoadView(FormView):
    template_name = 'manage_subject_load.html'
    form_class = CourseSearchForm  # Custom form for searching courses
    success_url = '/finalize_enrollment/<int:subject_load_list_id>/'

    def get_initial(self):
        # Get the student to be managed (passed in URL)
        student = get_object_or_404(Student, student_id=self.kwargs['student_id'])

        # Get the current academic year and semester
        current_year, current_semester = get_current_academic_term()

        # Create a Subject_Load_List if it doesn't exist for the student
        subject_load_list, created = Subject_Load_List.objects.get_or_create(
            student=student,
            school_year=current_year,
            semester=current_semester,
            defaults={'approval': False}
        )

        # Fetch the current subjects the student is enrolled in
        current_subjects = Subject_Load.objects.filter(subject_list=subject_load_list)
        
        # Gather details of the current subjects (offer number, course code, etc.)
        subject_details = []
        for subject_load in current_subjects:
            subject_offering = subject_load.subject
            schedule = DaySchedule.objects.filter(subject_offering=subject_offering)
            total_units = subject_offering.get_total_units()
            subject_details.append({
                'offer_code': subject_offering.offer_code,
                'course_code': subject_offering.course.course_code,
                'desc': subject_offering.course.desc,
                'instructor': subject_offering.instructor or '',
                'section': subject_offering.section,
                'room': subject_offering.room,
                'schedule': schedule,
                'total_units': total_units,
                'id': subject_load.id
            })

        # Return the student and their current subjects as part of the initial data
        return {
            'student': student,
            'subject_details': subject_details,
            'subject_load_list': subject_load_list,
        }

    def get_queryset(self):
        student = get_object_or_404(Student, student_id=self.kwargs['student_id'])
        current_year, current_semester = get_current_academic_term()

        # Fetch the Subject_Load_List for the student
        subject_load_list = Subject_Load_List.objects.filter(
            student=student,
            school_year=current_year,
            semester=current_semester
        ).first()

        # Get already enrolled subjects
        enrolled_subject_ids = Subject_Load.objects.filter(
            subject_list=subject_load_list
        ).values_list('subject_id', flat=True) if subject_load_list else []

        # Filter available courses
        available_courses = Subject_Offering.objects.filter(
            offer_year__lte=student.year_level,
            offer_sem=current_semester
        ).exclude(id__in=enrolled_subject_ids)

        # Apply search query
        query = self.request.GET.get('q', '')
        if query:
            available_courses = available_courses.filter(
                Q(offer_code__icontains=query) |
                Q(course__course_code__icontains=query) |
                Q(course__desc__icontains=query)
            )

        return available_courses

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        student = get_object_or_404(Student, student_id=self.kwargs['student_id'])
        kwargs['student'] = student  # Pass the student instance to the form
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, student_id=self.kwargs['student_id'])
        context['student'] = student  # Add the student object to the context
        context.update(self.get_initial())  # Add initial data to the context
        context['subject_load_list'] = self.get_initial()['subject_load_list']
        return context
    
    def form_valid(self, form):
        # Get the student to be managed (passed in URL)
        student = get_object_or_404(Student, id=self.kwargs['student_id'])
        
        # Get the selected course from the form
        selected_course_id = form.cleaned_data['selected_course']
        subject_offering = get_object_or_404(Subject_Offering, id=selected_course_id)

        # Get or create the Subject_Load_List for this student
        current_year, current_semester = get_current_academic_term()
        subject_load_list, created = Subject_Load_List.objects.get_or_create(
            student=student,
            school_year=current_year,
            semester=current_semester,
            defaults={'approval': False}
        )

        # Add the selected subject to the student's load
        Subject_Load.objects.create(subject_list=subject_load_list, subject=subject_offering)

        # Return the success URL after adding the course
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the current user is a student and if they already have an approved Subject_Load_List
        if request.user.user_type == 'student':
            student = get_object_or_404(Student, student_id=self.kwargs['student_id'])
            current_year, current_semester = get_current_academic_term()

            subject_load_list = Subject_Load_List.objects.filter(
                student=student,
                school_year=current_year,
                semester=current_semester,
                approval=True 
            ).first()

            if subject_load_list:
                return redirect('finalize_enrollment', subject_load_list_id=subject_load_list.id)
        
        return super().dispatch(request, *args, **kwargs)
    
def search_courses(request):
    query = request.GET.get('q', '')
    student_id = request.GET.get('student_id')
    student = get_object_or_404(Student, student_id=student_id)
    current_year, current_semester = get_current_academic_term()

    # Get all courses for the current semester and student's year level
    courses = Subject_Offering.objects.filter(
        course__offer_year__lte=student.year_level,
        course__offer_sem=current_semester,
        academic_year=current_year
    )

    # Apply the search query if provided
    if query:
        courses = courses.filter(
            Q(offer_code__icontains=query) | 
            Q(course__course_code__icontains=query) | 
            Q(course__desc__icontains=query)
        )

    results = []
    for course in courses:
        schedule = DaySchedule.objects.filter(subject_offering=course)
        schedule_str = ', '.join([f"{sch.day.name}: {sch.start_time.strftime('%I:%M %p')} - {sch.end_time.strftime('%I:%M %p')}" for sch in schedule])
        results.append({
            'id': course.pk,
            'offer_code': course.offer_code,
            'course_code': course.course.course_code,
            'desc': course.course.desc,
            'instructor': str(course.instructor) if course.instructor else None,
            'section': course.section,
            'room': course.room,
            'schedule': schedule_str,
            'total_units': course.course.get_total_units()
        })
    return JsonResponse({'results': results})

@csrf_exempt
def enroll_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            offer_code = data.get('offer_code')
            student_id = data.get('student_id')

            student = get_object_or_404(Student, student_id=student_id)
            subject_offering = get_object_or_404(Subject_Offering, offer_code=offer_code)

            # Get the current academic term
            current_year, current_semester = get_current_academic_term()

            # Get or create the Subject_Load_List
            subject_load_list, created = Subject_Load_List.objects.get_or_create(
                student=student,
                school_year=current_year,
                semester=current_semester,
                defaults={'approval': False}
            )

            # Add the selected subject offering to the student's load
            Subject_Load.objects.create(subject_list=subject_load_list, subject=subject_offering)

            subject_load_list.approval = False
            subject_load_list.save()

            # Fetch updated lists
            enrolled_subjects = Subject_Load.objects.filter(subject_list=subject_load_list)
            available_courses = Subject_Offering.objects.filter(
                course__offer_year__lte=student.year_level,
                course__offer_sem=current_semester
            ).exclude(id__in=enrolled_subjects.values_list('subject', flat=True))

            # Serialize data for response
            enrolled_data = [
                {
                    'id': subject.id,
                    'offer_code': subject.subject.offer_code,
                    'course_code': subject.subject.course.course_code,
                    'desc': subject.subject.course.desc,
                    'instructor': str(subject.subject.instructor) if subject.subject.instructor else None,
                    'section': subject.subject.section,
                    'room': subject.subject.room,
                    'schedule': ', '.join(
                        f"{sched.day.name}: {sched.start_time.strftime('%I:%M %p')} - {sched.end_time.strftime('%I:%M %p')}"
                        for sched in subject.subject.day_schedules.all()
                    ),
                    'total_units': subject.subject.get_total_units(),
                }
                for subject in enrolled_subjects
            ]

            available_data = [
                {
                    'id': course.offer_code,
                    'offer_code': course.offer_code,
                    'course_code': course.course.course_code,
                    'desc': course.course.desc,
                    'instructor': str(course.instructor) if course.instructor else None,
                    'section': course.section,
                    'room': course.room,
                    'schedule': ', '.join(
                        f"{sched.day.name}: {sched.start_time.strftime('%I:%M %p')} - {sched.end_time.strftime('%I:%M %p')}"
                        for sched in course.day_schedules.all()
                    ),
                    'total_units': course.get_total_units(),
                }
                for course in available_courses
            ]
            return JsonResponse({"status": "success", "success": True, "message": "Enrolled successfully"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def unenroll_course(request):
    if request.method == "POST":
        try:
            data = request.POST
            subject_load_id = data.get("subject_load_id")
            if not subject_load_id:
                return JsonResponse({"status": "error", "message": "Missing subject_load_id"}, status=400)
            
            subject_load = Subject_Load.objects.get(id=subject_load_id)
            student = subject_load.subject_list.student
            subject_offering = subject_load.subject

            # Delete the subject load
            subject_load.delete()

            # Fetch updated lists
            current_year, current_semester = get_current_academic_term()
            subject_load_list = Subject_Load_List.objects.filter(
                student=student,
                school_year=current_year,
                semester=current_semester
            ).first()

            subject_load_list.approval = False
            subject_load_list.save()

            enrolled_subjects = Subject_Load.objects.filter(subject_list=subject_load_list)
            available_courses = Subject_Offering.objects.filter(
                course__offer_year__lte=student.year_level,
                course__offer_sem=current_semester
            ).exclude(id__in=enrolled_subjects.values_list('subject', flat=True))

            # Serialize data for response
            enrolled_data = [
                {
                    'id': subject.id,
                    'offer_code': subject.subject.offer_code,
                    'course_code': subject.subject.course.course_code,
                    'desc': subject.subject.course.desc,
                    'instructor': str(subject.subject.instructor) if subject.subject.instructor else None,
                    'section': subject.subject.section,
                    'room': subject.subject.room,
                    'schedule': ', '.join(
                        f"{sched.day.name}: {sched.start_time.strftime('%I:%M %p')} - {sched.end_time.strftime('%I:%M %p')}"
                        for sched in subject.subject.day_schedules.all()
                    ),
                    'total_units': subject.subject.get_total_units(),
                }
                for subject in enrolled_subjects
            ]

            available_data = [
                {
                    'id': course.offer_code,
                    'offer_code': course.offer_code,
                    'course_code': course.course.course_code,
                    'desc': course.course.desc,
                    'instructor': str(course.instructor) if course.instructor else None,
                    'section': course.section,
                    'room': course.room,
                    'schedule': ', '.join(
                        f"{sched.day.name}: {sched.start_time.strftime('%I:%M %p')} - {sched.end_time.strftime('%I:%M %p')}"
                        for sched in course.day_schedules.all()
                    ),
                    'total_units': course.get_total_units(),
                }
                for course in available_courses
            ]
            return redirect('manage_subject_load', student_id=student.student_id)
            #return JsonResponse({"status": "success", "message": f"Unenrolled from subject load {subject_load_id}"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

#finalize enrollment (instructor approves of subject load list)
class FinalizeEnrollmentView(DetailView):
    model = Subject_Load_List
    template_name = 'finalize_enrollment.html'
    context_object_name = 'subject_load_list'

    def get_object(self):
        # Get the Subject_Load_List instance by ID
        subject_load_list = get_object_or_404(Subject_Load_List, id=self.kwargs['subject_load_list_id'])
        return subject_load_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user and related data
        user = self.request.user
        subject_load_list = context['subject_load_list']
        
        # Check if the user is a student or an instructor
        if user.user_type == 'student':
            # For student, show subjects in a read-only format with a message
            subject_details = []
            for subject_load in subject_load_list.subject_enrollments_items.all():
                subject_offering = subject_load.subject
                schedule = DaySchedule.objects.filter(subject_offering=subject_offering)
                total_units = subject_offering.get_total_units()
                subject_details.append({
                    'offer_code': subject_offering.offer_code,
                    'course_code': subject_offering.course.course_code,
                    'desc': subject_offering.course.desc,
                    'instructor': subject_offering.instructor or '',
                    'section': subject_offering.section,
                    'room': subject_offering.room,
                    'schedule': schedule,
                    'total_units': total_units,
                    'id': subject_load.id
                })
            context.update({
                'subject_details': subject_details,
                'message': "Your application is being reviewed. Please wait until approval."
            })
        
        elif user.user_type == 'instructor':
            # For instructor, show subjects with options to approve
            subject_details = []
            for subject_load in subject_load_list.subject_enrollments_items.all():
                subject_offering = subject_load.subject
                schedule = DaySchedule.objects.filter(subject_offering=subject_offering)
                total_units = subject_offering.get_total_units()
                subject_details.append({
                    'offer_code': subject_offering.offer_code,
                    'course_code': subject_offering.course.course_code,
                    'desc': subject_offering.course.desc,
                    'instructor': subject_offering.instructor or '',
                    'section': subject_offering.section,
                    'room': subject_offering.room,
                    'schedule': schedule,
                    'total_units': total_units,
                    'id': subject_load.id
                })
            context.update({
                'subject_details': subject_details,
                'message': "Please review and approve the student's enrollment."
            })

        return context

    def post(self, request, *args, **kwargs):
        subject_load_list = self.get_object()
        user = request.user
        
        if user.user_type == 'instructor' and 'approve' in request.POST:
            # Handle approval logic
            instructor = get_object_or_404(Instructor, user=user)
            subject_load_list.approval = True
            subject_load_list.approved_at = timezone.now()
            subject_load_list.approved_by = instructor
            subject_load_list.save()

            # Redirect after approval
            return redirect('select_student')

        # If no approval, just return the same page
        return self.get(request, *args, **kwargs)
    
#if student's subject load list was approved, summary page.
class EnrollmentSummaryView(DetailView):
    model = Subject_Load_List
    template_name = 'enrollment_summary.html'
    context_object_name = 'subject_load_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_loads = context['subject_load_list'].subject_enrollments_items.all()
        context['subject_loads'] = subject_loads
        return context

def generate_registration_forms_pdf(request, subject_load_list_id):
    subject_load_list = get_object_or_404(Subject_Load_List, id=subject_load_list_id)
    student = subject_load_list.student
    subject_details = Subject_Load.objects.filter(subject_list=subject_load_list)

    # Get the current semester and year
    current_semester = "1st Semester"  # You can dynamically set this based on your requirements
    current_year = datetime.now().year
    today = datetime.now().strftime('%m/%d/%Y')  # Current date

    # Calculate total units (based on your model structure)
    total_units = sum(course.subject.course.get_total_units() for course in subject_details)

    # Define the copy types
    copy_types = ['Registrar\'s Copy', 'Student\'s Copy', 'Dean\'s Copy', 'Cashier\'s Copy']
    
    template_path = finders.find('word_templates/form_templates.html')
    if not template_path:
            return HttpResponse("Template not found.", status=404)
    # Render the HTML for each form (one for each copy_type)
    html_content = ""
    for copy_type in copy_types:
        context = {
            'student': student,
            'courses': subject_details,
            'current_semester': current_semester,
            'current_year': current_year,
            'today': today,
            'total_units': total_units,
            'copy_type': copy_type,
            'choice': ['Old/Returnee', 'New/Transferee'],  # If applicable
        }
        with open(template_path, 'r') as file:
            template_content = file.read()

        template = Template(template_content)

        # Create a Django Context object and render the template
        rendered_content = template.render(Context(context))

        html_content += rendered_content
    
    options = {
        'page-size': 'Letter',  # Letter-size document
        'no-outline': None,
        'margin-top': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'margin-right': '0.5in',
    }

    # Render the full HTML content into a PDF using WeasyPrint
    pdf = pdfkit.from_string(html_content, False, options=options)


    # Return the PDF response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+student.user.last_name+'_registration_forms.pdf"'
    return response
