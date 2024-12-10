import django.db.models.deletion
from django.db import migrations, models

def create_default_dept(apps, schema_editor):
    Department = apps.get_model('user', 'Department')
    Department.objects.create(name="College of Computer Studies", shortname="CCS")
    Department.objects.create(name="College of Nursing and Midwifery", shortname="CONM")
    Department.objects.create(name="College of Medical Technology", shortname="CMT")
    Department.objects.create(name="College of Radiologic Technology", shortname="CRT")
    Department.objects.create(name="College of Arts and Sciences", shortname="CAS")
    Department.objects.create(name="College of Business Administration", shortname="CBA")
    Department.objects.create(name="College of Criminology", shortname="COC")
    Department.objects.create(name="College of Education", shortname="CED")
    Department.objects.create(name="College of Hospitality and Tourism Management", shortname="CHTM")
    Department.objects.create(name="Graduate School", shortname="GradSchool")
    Department.objects.create(name="Basic Education", shortname="BEd")
    Department.objects.create(name="NSTP & Research Office", shortname="NSTP")

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_dept)
    ]
