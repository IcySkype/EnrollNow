from django.contrib import admin
from .models import Course, Subject_Offering, DaySchedule,Subject_Load

admin.site.register(Course)
admin.site.register(Subject_Offering)
admin.site.register(DaySchedule)
admin.site.register(Subject_Load)