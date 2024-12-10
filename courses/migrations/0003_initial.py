import django.db.models.deletion
from django.db import migrations, models

def create_default_courses(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Department = apps.get_model('user', 'Department')

    
    ccs_department = Department.objects.get(shortname='CCS')
    cas_department = Department.objects.get(shortname='CAS')
    cba_department = Department.objects.get(shortname='CBA')
    ced_department = Department.objects.get(shortname='CED')
    nstp_department = Department.objects.get(shortname='NSTP')

    #BSIT Courses
    Course.objects.create(
        course_code="IT101", 
        desc="Info. Tech Fund. & Intro. to Computing", 
        units_lab=1, units_lec=2, offer_year=1, offer_sem="1st", department=ccs_department)
    Course.objects.create(
        course_code="IT102", 
        desc="Computer Programming 1", 
        units_lab=1, units_lec=2, offer_year=1, offer_sem="1st", department=ccs_department)
    Course.objects.create(
        course_code="GEU", 
        desc="Understanding the Self", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="1st", department=ccs_department)
    Course.objects.create(
        course_code="GER", 
        desc="Readings in Philippine History", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="1st", department=cas_department)
    Course.objects.create(
        course_code="GEC", 
        desc="The Contemporary World", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="1st", department=cas_department)
    Course.objects.create(
        course_code="Rizal", 
        desc="Life, Works, and Writings of Rizal", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="1st", department=cas_department)
    Course.objects.create(
        course_code="SFD", 
        desc="Student Formation & Development", 
        units_lab=0, units_lec=1, offer_year=1, offer_sem="1st", department=ced_department)
    Course.objects.create(
        course_code="PATH-FIT 1", 
        desc="Physical Activity Towards Health & Fitness 1 (Wellness & Fitness)", 
        units_lab=0, units_lec=2, offer_year=1, offer_sem="1st", department=cas_department)
    Course.objects.create(
        course_code="NSTP1", 
        desc="Foundation of Service 1", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="1st", department=nstp_department)

    it103 = Course.objects.create(
        course_code="IT103",
        desc="Computer Programming 2",
        units_lab=1, units_lec=2, offer_year=1, offer_sem="2nd", department=ccs_department)
    it103.prereq.set(Course.objects.filter(course_code="IT102"))

    itc101 = Course.objects.create(
        course_code="ITC101",
        desc="Intro. to Human Computer Interaction",
        units_lab=2,units_lec=1, offer_year=1, offer_sem="2nd", department=ccs_department)
    itc101.prereq.set(Course.objects.filter(course_code="IT101"))

    Course.objects.create(
        course_code="GEM",
        desc="Mathematics in the Modern World",
        units_lab=0, units_lec=3, offer_year=1, offer_sem="2nd", department=cas_department)

    Course.objects.create(
        course_code="GEP", desc="Purposive Communication", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="2nd", department=cas_department)

    Course.objects.create(
        course_code="GEA", desc="Art Appreciation", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="2nd", department=cas_department)
    
    Course.objects.create(
        course_code="GEE", desc="Ethics", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="2nd", department=cas_department)
    
    Course.objects.create(
        course_code="GES", desc="Science, Technology, and Society", 
        units_lab=0, units_lec=3, offer_year=1, offer_sem="2nd", department=cas_department)

    pathfit2 = Course.objects.create(
        course_code="PATH-FIT2",
        desc="Physical Activity Towards Health & Fitness 2",
        units_lab=0, units_lec=2, offer_year=1, offer_sem="2nd", department=cas_department)
    pathfit2.prereq.set(Course.objects.filter(course_code="PATH-FIT1"))

    nstp2 = Course.objects.create(
        course_code="NSTP2",
        desc="Social Awareness & Environment for Service 2",
        units_lab=0, units_lec=3, offer_year=1, offer_sem="2nd", department=nstp_department)
    nstp2.prereq.set(Course.objects.filter(course_code="NSTP1"))
    
    ms101 = Course.objects.create(
        course_code="MS101",
        desc="Discrete Mathematics",
        units_lab=0, units_lec=3, offer_year=1, offer_sem="Sum", department=cas_department)
    ms101.prereq.set(Course.objects.filter(course_code="GEM"))

    itp100 = Course.objects.create(
        course_code="ITP100",
        desc="Info. Tech. & Business Productivity",
        units_lab=1, units_lec=2, offer_year=1, offer_sem="Sum", department=ccs_department)
    itp100.prereq.set(Course.objects.filter(course_code="IT101"))

    cs201 = Course.objects.create(
        course_code="CS201",
        desc="Data Structures & Algorithm",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="1st", department=ccs_department)
    cs201.prereq.set(Course.objects.filter(course_code="IT103"))

    elec1 = Course.objects.create(
        course_code="ELEC1",
        desc="Object-Oriented and Event-Driven Programming",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="1st", department=ccs_department)
    elec1.prereq.set(Course.objects.filter(course_code="IT103"))

    cs206 = Course.objects.create(
        course_code="CS206",
        desc="Logic Design & Switching Theory",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="1st", department=ccs_department)
    cs206.prereq.set(Course.objects.filter(course_code="MS101"))
    
    freeelec1 = Course.objects.create(
        course_code="Free ELEC1",
        desc="Platform Technologies",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="1st", department=ccs_department)
    freeelec1.prereq.set(Course.objects.filter(course_code="IT101"))

    it104 = Course.objects.create(
        course_code="IT104",
        desc="Web Systems & Technologies",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="1st", department=ccs_department)
    it104.prereq.set(Course.objects.filter(course_code="IT103"))

    ms102 = Course.objects.create(
        course_code="MS102",
        desc="Modern Statistics (Probability & Random Variables)",
        units_lab=0, units_lec=3, offer_year=2, offer_sem="1st", department=cas_department)
    ms102.prereq.set(Course.objects.filter(course_code="GEM"))

    Course.objects.create(
        course_code="TEM",
        desc="The Entrepreneurial Mind",
        units_lab=0, units_lec=3, offer_year=2, offer_sem="1st", department=cba_department)

    Course.objects.create(
        course_code="QSS",
        desc="Quality Standard & Safety",
        units_lab=0, units_lec=3, offer_year=2, offer_sem="1st", department=ccs_department)

    pathfit3 = Course.objects.create(
        course_code="PATH-FIT3",
        desc="Physical Activity Towards Health & Fitness 3 (Aquatic)",
        units_lab=0, units_lec=2, offer_year=2, offer_sem="1st", department=cas_department)
    pathfit3.prereq.set(Course.objects.filter(course_code="PATH-FIT2"))
    
    cs211 = Course.objects.create(
        course_code="CS211",
        desc="Application Development & Emerging Tech",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="2nd", department=ccs_department)
    cs211.prereq.set(Course.objects.filter(course_code__in=["CS201", "ELEC1", "CS206"]))

    ms103 = Course.objects.create(
        course_code="MS103",
        desc="Quantitative Methods (Modeling & Simulation)",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="2nd", department=ccs_department)
    ms103.prereq.set(Course.objects.filter(course_code="ELEC1"))

    elec2 = Course.objects.create(
        course_code="ELEC2",
        desc="Integrative Programming & Technologies 1",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="2nd", department=ccs_department)
    elec2.prereq.set(Course.objects.filter(course_code__in=["CS201", "CS206"]))

    im101 = Course.objects.create(
        course_code="IM101",
        desc="Information Management",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="2nd", department=ccs_department)
    im101.prereq.set(Course.objects.filter(course_code="ITC101"))

    freeelec2 = Course.objects.create(
        course_code="Free ELEC2",
        desc="Human Computer Interaction 2",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="2nd", department=ccs_department)
    freeelec2.prereq.set(Course.objects.filter(course_code="IT101"))

    iot = Course.objects.create(
        course_code="IOT",
        desc="Internet of Things",
        units_lab=1, units_lec=2, offer_year=2, offer_sem="2nd", department=ccs_department)
    iot.prereq.set(Course.objects.filter(course_code__in=["CS201", "CS206"]))

    Course.objects.create(
        course_code="GS",
        desc="Gender & Society",
        units_lab=0, units_lec=3, offer_year=2, offer_sem="2nd", department=cas_department)

    Course.objects.create(
        course_code="PEEQ",
        desc="People & the Earth’s Ecosystem",
        units_lab=0, units_lec=3, offer_year=2, offer_sem="2nd", department=cas_department)

    pathfit4 = Course.objects.create(
        course_code="PATH-FIT4",
        desc="Physical Activity Towards Health & Fitness 4 (Outdoor & Adventure)",
        units_lab=0, units_lec=2, offer_year=2, offer_sem="2nd", department=cas_department)
    pathfit4.prereq.set(Course.objects.filter(course_code="PATH-FIT3"))

    cs311 = Course.objects.create(
        course_code="CS311",
        desc="Fundamentals of Database Systems",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="1st", department=ccs_department)
    cs311.prereq.set(Course.objects.filter(course_code="IM101"))

    net101 = Course.objects.create(
        course_code="Net101",
        desc="Network Design & Management",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="1st", department=ccs_department)
    net101.prereq.set(Course.objects.filter(course_code="CS206"))

    cs310 = Course.objects.create(
        course_code="CS310",
        desc="Systems Integration and Architecture 1",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="1st", department=ccs_department)
    cs310.prereq.set(Course.objects.filter(course_code="IM101"))

    Course.objects.create(
        course_code="CS304",
        desc="Trends, Issues, Seminars & Field Trips in IT",
        units_lab=0, units_lec=3, offer_year=3, offer_sem="1st", department=ccs_department)

    elec3 = Course.objects.create(
        course_code="ELEC3",
        desc="Integrative Programming & Technologies 2",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="1st", department=ccs_department)
    elec3.prereq.set(Course.objects.filter(course_code="ELEC2"))

    cs303 = Course.objects.create(
        course_code="CS303",
        desc="Systems Analysis & Design",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="1st", department=ccs_department)
    cs303.prereq.set(Course.objects.filter(course_code="CS211"))

    rcit = Course.objects.create(
        course_code="RCIT",
        desc="Research & Communication in IT",
        units_lab=0, units_lec=3, offer_year=3, offer_sem="1st", department=ccs_department)
    rcit.prereq.set(Course.objects.filter(course_code="IM101"))

    net102 = Course.objects.create(
        course_code="Net102",
        desc="Network Advanced Security",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="2nd", department=ccs_department)
    net102.prereq.set(Course.objects.filter(course_code="Net101"))

    cs312 = Course.objects.create(
        course_code="CS312",
        desc="Advanced Database Systems",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="2nd", department=ccs_department)
    cs312.prereq.set(Course.objects.filter(course_code="CS311"))

    cs313 = Course.objects.create(
        course_code="CS313",
        desc="Information Assurance and Security 1",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="2nd", department=ccs_department)
    cs313.prereq.set(Course.objects.filter(course_code="CS311"))

    cs314 = Course.objects.create(
        course_code="CS314",
        desc="Systems Administration & Maintenance",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="2nd", department=ccs_department)
    cs314.prereq.set(Course.objects.filter(course_code="CS311"))

    freeelec3 = Course.objects.create(
        course_code="Free ELEC3",
        desc="Web Management Systems & Security",
        units_lab=1, units_lec=2, offer_year=3, offer_sem="2nd", department=ccs_department)
    freeelec3.prereq.set(Course.objects.filter(course_code="CS211"))

    Course.objects.create(
        course_code="SocProf",
        desc="Social and Professional Issues",
        units_lab=0, units_lec=3, offer_year=3, offer_sem="2nd", department=ccs_department)

    cap101 = Course.objects.create(
        course_code="Cap101",
        desc="Capstone Project & Research 1 (Proposal & Design)",
        units_lab=2, units_lec=2, offer_year=3, offer_sem="2nd", department=ccs_department)
    cap101.prereq.set(Course.objects.filter(course_code__in=["CS303", "CS311"]))
    
    cs412 = Course.objects.create(
        course_code="CS412",
        desc="Information Assurance & Security 2",
        units_lab=1, units_lec=2, offer_year=4, offer_sem="1st", department=ccs_department)
    cs412.prereq.set(Course.objects.filter(course_code="CS313"))

    cs401 = Course.objects.create(
        course_code="CS401",
        desc="IT Project Management",
        units_lab=1, units_lec=2, offer_year=4, offer_sem="1st", department=ccs_department)
    cs401.prereq.set(Course.objects.filter(course_code="CS303"))

    cap102 = Course.objects.create(
        course_code="Cap102",
        desc="Capstone Project & Research 2 (Implementation)",
        units_lab=2, units_lec=2, offer_year=4, offer_sem="1st", department=ccs_department)
    cap102.prereq.set(Course.objects.filter(course_code="Cap101"))

    elec4 = Course.objects.create(
        course_code="ELEC4",
        desc="Systems Integration and Architecture 2",
        units_lab=1, units_lec=2, offer_year=4, offer_sem="1st", department=ccs_department)
    elec4.prereq.set(Course.objects.filter(course_code="CS310"))
    
    it400 = Course.objects.create(
        course_code="IT400",
        desc="Practicum",
        units_lab=0, units_lec=9, offer_year=4, offer_sem="2nd", department=ccs_department
    )

    it400.prereq.set(
        Course.objects.filter(
            course_code__in=[
                "IT101", "IT102", "GEU", "GER", "GEC", "Rizal", "SFD", "PATH-FIT1", "NSTP1",
                "IT103", "ITC101", "GEM", "GEP", "GEA", "GEE", "GES", "PATH-FIT2", "NSTP2", "MS101", "ITP100",
                "CS201", "ELEC1", "CS206", "Free ELEC1", "IT104", "MS102", "TEM", "QSS", "PATH-FIT3",
                "CS211", "MS103", "ELEC2", "IM101", "Free ELEC2", "IOT", "GS", "PEEQ", "PATH-FIT4",
                "CS311", "Net101", "CS310", "CS304", "ELEC3", "CS303", "RCIT",
                "Net102", "CS312", "CS313", "CS314", "Free ELEC3", "SocProf", "Cap101",
                "CS412", "CS401", "Cap102", "ELEC4"
            ]
        )
    )

def create_days(apps, schema_editor):
    Day = apps.get_model('courses', 'Day')
    Day.objects.create(name="Sunday")
    Day.objects.create(name="Monday")
    Day.objects.create(name="Tuesday")
    Day.objects.create(name="Wednesday")
    Day.objects.create(name="Thursday")
    Day.objects.create(name="Friday")
    Day.objects.create(name="Saturday")

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0002_initial'),
        ('user', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_courses),
        migrations.RunPython(create_days)
    ]
