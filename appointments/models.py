from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from django.db.models import Q
from django.core.exceptions import ValidationError
from courses.models import Subject_Load, Subject_Offering
from user.models import Student, Instructor
from courses.helper import get_current_academic_term
from django.utils.timezone import now

class ConsultationRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='consultation_requests')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='consultation_requests')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Consultation: {self.student} with {self.instructor} on {self.date} ({self.start_time}-{self.end_time})"
    
    def approve(self):
        self.approved = True
        self.approved_at = datetime.now()
        self.save()
