from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=10)
    
    def __str__(self):
        return self.shortname
    
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    first_name = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True) #possible no middle name
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.middlename:
            return f"{self.first_name} {self.middlename}-{self.last_name}"
        else: 
            return f"{self.first_name} {self.last_name}"
        
    def clean(self):
        super().clean()
        if self.user_type == 'student' and hasattr(self, 'instructor'):
            raise ValidationError("A user cannot be both a student and an instructor.")
        if self.user_type == 'instructor' and hasattr(self, 'student'):
            raise ValidationError("A user cannot be both an instructor and a student.")

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': 'student'})
    degree_program = models.CharField(max_length=50)
    year_level = models.PositiveIntegerField(default=1)
    student_id = models.CharField(max_length=10, help_text="ID Number", unique=True)

    # Enrollment Information
    enrollment_status = models.CharField(max_length=20, null=True, blank=True, default='unenrolled')
    last_enrolled_year = models.PositiveIntegerField(null=True, blank=True)
    last_enrolled_semester = models.CharField(max_length=3, choices=[
                                                ('1st', '1st Semester'),
                                                ('2nd', '2nd Semester'),
                                                ('Sum', 'Summer Semester')
                                            ], default='1st')
    
    # Personal Information
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    civil_status = models.CharField(max_length=20)
    address = models.TextField()
    present_address = models.TextField()
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    tribe = models.CharField(max_length=50, null=True, blank=True)

    # Parent/Guardian Information
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=50)
    parent_address = models.TextField()
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_relation = models.CharField(max_length=50, null=True, blank=True)
    guardian_address = models.TextField(null=True, blank=True)

    # Educational Background
    elementary_school_name = models.CharField(max_length=100)
    elementary_school_address = models.TextField()
    elementary_graduate_year = models.PositiveIntegerField()
    secondary_school_name = models.CharField(max_length=100)
    secondary_school_address = models.TextField()
    secondary_graduate_year = models.PositiveIntegerField()
    collegiate_school_name = models.CharField(max_length=100, null=True, blank=True)
    collegiate_school_address = models.TextField(null=True, blank=True)
    collegiate_graduate_year = models.PositiveIntegerField(null=True, blank=True)
    collegiate_degree_completed = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(year_level__gte=1), name='valid_year_level'),
        ]

    def __str__(self):
        if self.user.middlename:
            return f"{self.user.first_name} {self.user.middlename[0]}. {self.user.last_name}"
        else:
            return f"{self.user.first_name} {self.user.last_name}"

    def __repr__(self):
        return f"Student(id={self.student_id}, first_name='{self.user.first_name}', last_name='{self.user.last_name}', degree_program='{self.degree_program}', year_level='{self.year_level}', department='{self.user.department}')"
    
    def clean(self):
        if self.user.user_type != 'student':
            raise ValidationError("The linked user must be of type 'student'.")

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': 'instructor'})
    instructor_id = models.CharField(max_length=10, help_text="ID Number", unique=True)
    is_department_head = models.BooleanField(default=False)

    def __str__(self):
        if self.user.middlename:
            return f"{self.user.first_name} {self.user.middlename[0]}. {self.user.last_name}"
        else:
            return f"{self.user.first_name} {self.user.last_name}"

    def __repr__(self):
        return f"Student(id={self.id}, first_name='{self.user.first_name}', last_name='{self.user.last_name}', department='{self.user.department}')"
    
    def clean(self):
        if self.user.user_type != 'instructor':
            raise ValidationError("The linked user must be of type 'instructor'.")