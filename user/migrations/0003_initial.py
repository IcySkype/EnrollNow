import django.db.models.deletion
import datetime
from django.db import migrations, models

def create_default_users(apps, schema_editor):
    User = apps.get_model('user', 'User')
    Student = apps.get_model('user', 'Student')
    Instructor = apps.get_model('user', 'Instructor')
    Department = apps.get_model('user', 'Department')
    ccs_department = Department.objects.get(shortname='CCS')

    student_user = User.objects.create_user(
        username='JohnDoe2020',
        password='fruitsalad3',
        email='student@example.com',
        first_name='John',
        last_name='Doe',
        user_type='student',
        department=ccs_department
    )

    Student.objects.create(
        user=student_user,
        degree_program = "BS Information Technology",
        year_level = 1,
        student_id = "2020-123A5",
        last_enrolled_year = 2020,
        sex = 'Male',
        civil_status = 'Single',
        address = 'Somewhere, Iligan City',
        present_address = 'Somewhere, Over The Rainbow City',
        birthdate = datetime.datetime(2020, 5, 17),
        birthplace = 'In a hospital',
        nationality = 'Alien',
        religion = 'Church of the Sun',

        father_name = 'R2D2',
        father_occupation = 'Robot',
        mother_name = 'Michelle Jackydaughter',
        mother_occupation = 'Songwriter',
        parent_address = 'Moon',

        elementary_school_name = 'Sundae School',
        elementary_school_address = 'Ice cream road, Dessert City',
        elementary_graduate_year = 1996,
        secondary_school_name = "Xaviers School for  Gifted Youngsters",
        secondary_school_address = 'X-men',
        secondary_graduate_year = 2010,
    )

     # Create an instructor user
    instructor_user = User.objects.create_user(
        username='ProfessorX',
        password='xmenorigins',
        email='instructor@example.com',
        first_name='Charles',
        last_name='Xavier',
        user_type='instructor'
    )

    Instructor.objects.create(
        user=instructor_user,
        instructor_id = '123222x',
        is_department_head = True,
        department=ccs_department
    )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_users)
    ]
