from django import forms
from .models import ConsultationRequest
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q
from courses.helper import get_current_academic_term
from courses.models import Subject_Load,Subject_Offering

class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['instructor', 'date', 'start_time', 'end_time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user argument and remove it from kwargs
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.user:
            self.instance.student = self.user.student      

        # Ensure the date is not today or in the past
        if self.instance.date <= datetime.now().date():
            raise ValidationError("Consultation requests must be scheduled at least one day in advance.")

        # Ensure the time is within allowed hours (8am-12pm, 1pm-5pm)
        if not (datetime.strptime("08:00", "%H:%M").time() <= self.instance.start_time < datetime.strptime("12:00", "%H:%M").time() or
                datetime.strptime("13:00", "%H:%M").time() <= self.instance.start_time < datetime.strptime("17:00", "%H:%M").time()):
            raise ValidationError("Consultation time must be between 8am-12pm or 1pm-5pm.")

        # Get the current academic year and semester
        academic_year, current_semester = get_current_academic_term()

        # Ensure no overlapping consultation schedules
        overlapping = ConsultationRequest.objects.filter(
            Q(student=self.instance.student) | Q(instructor=self.instance.instructor),
            date=self.instance.date,
            start_time__lt=self.instance.end_time,
            end_time__gt=self.instance.start_time,
        ).exclude(id=self.instance.id)
        
        if overlapping.exists():
            raise ValidationError("This schedule conflicts with an existing consultation.")

        # Check for conflicts with Subject_Load schedules within the current academic term
        student_subject_conflicts = Subject_Load.objects.filter(
            subject_list__student=self.user.student,
            subject_list__school_year=academic_year,
            subject_list__semester=current_semester,
            subject__day_schedules__day__name=self.instance.date.strftime("%A"),
            subject__day_schedules__start_time__lt=self.instance.end_time,
            subject__day_schedules__end_time__gt=self.instance.start_time,
        )

        instructor_subject_conflicts = Subject_Offering.objects.filter(
            instructor=self.instance.instructor,
            academic_year=academic_year,
            semester=current_semester,
            day_schedules__day__name=self.instance.date.strftime("%A"),
            day_schedules__start_time__lt=self.instance.end_time,
            day_schedules__end_time__gt=self.instance.start_time,
        )

        if student_subject_conflicts.exists():
            raise ValidationError("The consultation conflicts with the student's class schedule.")
        
        if instructor_subject_conflicts.exists():
            raise ValidationError("The consultation conflicts with the instructor's class schedule.")
        
        # If commit is True, save the instance
        if commit:
            self.instance.save()

        return self.instance