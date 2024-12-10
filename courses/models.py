from django.db import models
from django.core.exceptions import ValidationError
from user.models import Department, Instructor, Student
from datetime import time
import uuid

class Course(models.Model):
    course_code = models.CharField(max_length=15)
    desc = models.CharField(max_length=100)
    units_lab = models.PositiveIntegerField(default = 0)
    units_lec = models.PositiveIntegerField(default = 3)
    offer_year = models.PositiveIntegerField(default = 1)
    offer_sem = models.CharField(max_length=3, choices=[
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('Sum', 'Summer Semester')
    ])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='course_offerings')
    prereq = models.ManyToManyField('self', blank=True, symmetrical=False)#many to many self reference. 'blank=True' = optional
    
    def __str__(self):
        return self.course_code
    
    def __repr__(self):
        prereqs = ', '.join([course.course_code for course in self.prereq.all()])
        return f"Course(course_code={self.course_code}, desc='{self.desc}', prereqs=[{prereqs}])"

    def get_total_units(self):
        return self.units_lab + self.units_lec

class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Subject_Offering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, null=True, blank=True, on_delete=models.SET_NULL)
    offer_code = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    room = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=9, default='2023-2024')  # Format: '2023-2024'
    semester = models.CharField(max_length=3, choices=[
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('Sum', 'Summer Semester')
    ], default='1st')

    def __str__(self):
        return f"{self.course} - {self.offer_code}"
    
    def get_total_units(self):
        return self.course.get_total_units()

class DaySchedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject_offering = models.ForeignKey(Subject_Offering, on_delete=models.CASCADE, related_name='day_schedules')

    def __str__(self):
        return f"{self.day.name}: {self.start_time} - {self.end_time}"

class Subject_Load_List(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_enrollments')
    school_year = models.CharField(max_length=9)  # Format: '2023-2024'
    semester = models.CharField(max_length=3, choices=[
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('Sum', 'Summer Semester')
    ])
    approval = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student} - SY{self.school_year} Sem{self.semester}"
    
class Subject_Load(models.Model):
    subject_list = models.ForeignKey(Subject_Load_List, on_delete=models.CASCADE, related_name='subject_enrollments_items')
    subject = models.ForeignKey(Subject_Offering, on_delete=models.CASCADE)
    id = models.UUIDField(default = uuid.uuid1, unique = True, primary_key = True)

    class Meta:
        unique_together = ('subject_list', 'subject')
    
    def __str__(self):
        return f"{self.subject_list.student} : {self.subject}"