from django import forms
from django.forms.models import inlineformset_factory
from django.db.models import Q
from .models import Subject_Offering, Course, Day, Subject_Load, DaySchedule
from .helper import get_current_academic_term
from datetime import datetime
from user.models import Student, Instructor

DayScheduleFormSet = inlineformset_factory(
    Subject_Offering,
    DaySchedule,
    fields=('day', 'start_time', 'end_time'),
    extra=0,
    can_delete=True 
)

class SubjectOfferingForm(forms.ModelForm):
    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Days"
    )
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Instructor"
    )

    class Meta:
        model = Subject_Offering
        fields = ['course', 'offer_code', 'section', 'room', 'days', 'instructor']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        current_academic_year, current_semester = get_current_academic_term()
        instance.academic_year = current_academic_year
        instance.semester = current_semester
        if commit:
            instance.save()
        return instance

    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields  = '__all__'
        widgets = {
            'prereq': forms.SelectMultiple(attrs={
                'class': 'form-control select2',  # Add class for Select2 initialization
            })
        }

    def clean_prereq(self):
        prereqs = self.cleaned_data.get('prereq', [])
        if self.instance in prereqs:
            raise forms.ValidationError("A course cannot be a prerequisite for itself.")
        return prereqs

class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="First Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter First Name',
        'class': 'form-control'
    }))
    middlename = forms.CharField(max_length=30, required=False, label="Middle Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Middle Name (Optional)',
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=30, label="Last Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Last Name',
        'class': 'form-control'
    }))
    class Meta:
        model = Student
        fields = ['year_level', 'first_name', 'middlename', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        student = super().save(commit=False)
        user = student.user
        updated = False

        # Only update user fields if necessary
        if user.first_name != self.cleaned_data['first_name']:
            user.first_name = self.cleaned_data['first_name']
            updated = True
        if user.middle_name != self.cleaned_data['middle_name']:
            user.middle_name = self.cleaned_data['middle_name']
            updated = True
        if user.last_name != self.cleaned_data['last_name']:
            user.last_name = self.cleaned_data['last_name']
            updated = True

        if updated:
            user.save()
        if commit:
            student.save()
        return student

class CourseSearchForm(forms.Form):
    query = forms.CharField(required=False, label="Search for a course", max_length=100)
    selected_course = forms.ModelChoiceField(queryset=Subject_Offering.objects.none(), required=False, label="Select Course")
    
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        
        if student:
            # Get current academic year and semester
            current_year, current_semester = get_current_academic_term()

            # Filter available courses
            available_courses = Subject_Offering.objects.filter(
                course__offer_year__lte=student.year_level,
                course__offer_sem=current_semester
            )

            # Apply search query if provided
            query = self.data.get('query', '')  # Use self.data to get query from form data
            if query:
                available_courses = available_courses.filter(
                    Q(offer_code__icontains=query) | 
                    Q(course__course_code__icontains=query) | 
                    Q(course__desc__icontains=query)
                )

            self.fields['selected_course'].queryset = available_courses