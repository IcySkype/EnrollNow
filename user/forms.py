from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Student, Instructor, Department

User = get_user_model()

class StudentSignUpForm(UserCreationForm):
    # Fields for User model
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
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Username',
        'class': 'form-control'
    }))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    # Fields specific to Student model
    degree_program = forms.CharField(max_length=50, label="Degree Program", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Degree Program',
        'class': 'form-control'
    }))
    year_level = forms.IntegerField(label="Year Level", widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Year Level',
        'class': 'form-control'
    }))
    student_id = forms.CharField(max_length=10, label="Student ID", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Student ID',
        'class': 'form-control'
    }))
    
    last_enrolled_year = forms.IntegerField(required=False, label="Last Enrolled Year", widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Last Enrolled Year (Optional)',
        'class': 'form-control'
    }))
    last_enrolled_semester = forms.ChoiceField(
        choices=[
            ('1st', '1st Semester'),
            ('2nd', '2nd Semester'),
            ('Sum', 'Summer Semester')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label="Last Enrolled Semester"
    )
    sex = forms.ChoiceField(choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], label="Sex", widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    civil_status = forms.CharField(max_length=20, label="Civil Status", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Civil Status',
        'class': 'form-control'
    }))
    address = forms.CharField(max_length=255, label="Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Address',
        'class': 'form-control'
    }))
    present_address = forms.CharField(max_length=255, label="Present Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Present Address',
        'class': 'form-control'
    }))
    birthdate = forms.DateField(label="Birthdate", widget=forms.DateInput(attrs={
        'placeholder': 'Select Birthdate',
        'type': 'date',
        'class': 'form-control'
    }))
    birthplace = forms.CharField(max_length=100, label="Birthplace", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Birthplace',
        'class': 'form-control'
    }))
    nationality = forms.CharField(max_length=50, label="Nationality", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Nationality',
        'class': 'form-control'
    }))
    religion = forms.CharField(max_length=50, label="Religion", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Religion',
        'class': 'form-control'
    }))
    tribe = forms.CharField(max_length=50, required=False, label="Tribe", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Tribe (Optional)',
        'class': 'form-control'
    }))

    father_name = forms.CharField(max_length=100, label="Father's Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Father\'s Name',
        'class': 'form-control'
    }))
    father_occupation = forms.CharField(max_length=50, label="Father's Occupation", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Father\'s Occupation',
        'class': 'form-control'
    }))
    mother_name = forms.CharField(max_length=100, label="Mother's Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Mother\'s Name',
        'class': 'form-control'
    }))
    mother_occupation = forms.CharField(max_length=50, label="Mother's Occupation", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Mother\'s Occupation',
        'class': 'form-control'
    }))
    parent_address = forms.CharField(max_length=255, label="Parent Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Parent Address',
        'class': 'form-control'
    }))
    guardian_name = forms.CharField(max_length=100, required=False, label="Guardian's Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Guardian\'s Name (Optional)',
        'class': 'form-control'
    }))
    guardian_relation = forms.CharField(max_length=50, required=False, label="Guardian Relation", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Guardian Relation (Optional)',
        'class': 'form-control'
    }))
    guardian_address = forms.CharField(max_length=255, required=False, label="Guardian Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Guardian Address (Optional)',
        'class': 'form-control'
    }))

    elementary_school_name = forms.CharField(max_length=100, label="Elementary School Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Elementary School Name',
        'class': 'form-control'
    }))
    elementary_school_address = forms.CharField(max_length=255, label="Elementary School Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Elementary School Address',
        'class': 'form-control'
    }))
    elementary_graduate_year = forms.IntegerField(label="Elementary Graduation Year", widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Elementary Graduation Year',
        'class': 'form-control'
    }))
    secondary_school_name = forms.CharField(max_length=100, label="Secondary School Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Secondary School Name',
        'class': 'form-control'
    }))
    secondary_school_address = forms.CharField(max_length=255, label="Secondary School Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Secondary School Address',
        'class': 'form-control'
    }))
    secondary_graduate_year = forms.IntegerField(label="Secondary Graduation Year", widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Secondary Graduation Year',
        'class': 'form-control'
    }))
    collegiate_school_name = forms.CharField(max_length=100, required=False, label="Collegiate School Name", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Collegiate School Name (Optional)',
        'class': 'form-control'
    }))
    collegiate_school_address = forms.CharField(max_length=255, required=False, label="Collegiate School Address", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Collegiate School Address (Optional)',
        'class': 'form-control'
    }))
    collegiate_graduate_year = forms.IntegerField(required=False, label="Collegiate Graduation Year", widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Collegiate Graduation Year (Optional)',
        'class': 'form-control'
    }))
    collegiate_degree_completed = forms.CharField(max_length=100, required=False, label="Collegiate Degree Completed", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Collegiate Degree Completed (Optional)',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'middlename', 'last_name', 'department', 'degree_program', 'year_level', 'student_id',
                  'last_enrolled_year', 'last_enrolled_semester', 'sex', 'civil_status', 'address',
                  'present_address', 'birthdate', 'birthplace', 'nationality', 'religion', 'tribe',
                  'father_name', 'father_occupation', 'mother_name', 'mother_occupation', 'parent_address',
                  'guardian_name', 'guardian_relation', 'guardian_address', 'elementary_school_name',
                  'elementary_school_address', 'elementary_graduate_year', 'secondary_school_name',
                  'secondary_school_address', 'secondary_graduate_year', 'collegiate_school_name',
                  'collegiate_school_address', 'collegiate_graduate_year', 'collegiate_degree_completed','username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        user.save()

        if commit:
            student = Student.objects.create(user=user,
                                            degree_program=self.cleaned_data['degree_program'],
                                            year_level=self.cleaned_data['year_level'],
                                            student_id=self.cleaned_data['student_id'],
                                            last_enrolled_year=self.cleaned_data['last_enrolled_year'],
                                            last_enrolled_semester=self.cleaned_data['last_enrolled_semester'],
                                            sex=self.cleaned_data['sex'],
                                            civil_status=self.cleaned_data['civil_status'],
                                            address=self.cleaned_data['address'],
                                            present_address=self.cleaned_data['present_address'],
                                            birthdate=self.cleaned_data['birthdate'],
                                            birthplace=self.cleaned_data['birthplace'],
                                            nationality=self.cleaned_data['nationality'],
                                            religion=self.cleaned_data['religion'],
                                            tribe=self.cleaned_data['tribe'],
                                            father_name=self.cleaned_data['father_name'],
                                            father_occupation=self.cleaned_data['father_occupation'],
                                            mother_name=self.cleaned_data['mother_name'],
                                            mother_occupation=self.cleaned_data['mother_occupation'],
                                            parent_address=self.cleaned_data['parent_address'],
                                            guardian_name=self.cleaned_data['guardian_name'],
                                            guardian_relation=self.cleaned_data['guardian_relation'],
                                            guardian_address=self.cleaned_data['guardian_address'],
                                            elementary_school_name=self.cleaned_data['elementary_school_name'],
                                            elementary_school_address=self.cleaned_data['elementary_school_address'],
                                            elementary_graduate_year=self.cleaned_data['elementary_graduate_year'],
                                            secondary_school_name=self.cleaned_data['secondary_school_name'],
                                            secondary_school_address=self.cleaned_data['secondary_school_address'],
                                            secondary_graduate_year=self.cleaned_data['secondary_graduate_year'],
                                            collegiate_school_name=self.cleaned_data['collegiate_school_name'],
                                            collegiate_school_address=self.cleaned_data['collegiate_school_address'],
                                            collegiate_graduate_year=self.cleaned_data['collegiate_graduate_year'],
                                            collegiate_degree_completed=self.cleaned_data['collegiate_degree_completed']
                                            )
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        year_level = cleaned_data.get("year_level")
        if year_level <= 0:
            raise forms.ValidationError("Year level must be a positive integer.")
        return cleaned_data

class InstructorSignUpForm(UserCreationForm):
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
    
    instructor_id = forms.CharField(max_length=10, label="Instructor ID", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Instructor ID',
        'class': 'form-control'
    }))
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Department",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'placeholder': 'Select Department',
        })
    )
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        'placeholder': 'Enter Username',
        'class': 'form-control'
    }))
    class Meta:
        model = User
        fields = ['first_name', 'middlename', 'last_name', 'instructor_id', 'department', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'instructor'
        user.save()

        if commit:
            Instructor.objects.create(user=user, 
                                      instructor_id=self.cleaned_data['instructor_id'])
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'middlename', 'last_name', 'email', 'department']
        exclude = ['username', 'password', 'user_type']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'degree_program', 'year_level', 'student_id', 'sex', 'civil_status',
            'address', 'present_address', 'birthdate', 'birthplace', 'nationality',
            'religion', 'tribe', 'father_name', 'father_occupation', 'mother_name',
            'mother_occupation', 'parent_address', 'guardian_name', 'guardian_relation',
            'guardian_address', 'elementary_school_name', 'elementary_school_address',
            'elementary_graduate_year', 'secondary_school_name', 'secondary_school_address',
            'secondary_graduate_year', 'collegiate_school_name', 'collegiate_school_address',
            'collegiate_graduate_year', 'collegiate_degree_completed'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['birthdate'].widget = forms.DateInput(attrs={'type': 'date'})

class InstructorEditForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['instructor_id', 'is_department_head']