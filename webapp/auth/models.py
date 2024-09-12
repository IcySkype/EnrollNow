from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import secrets

class MyUserManager(BaseUserManager):
  """
  Custom user manager to create different user types.
  """
  def create_user(self, school_id, first_name, surname, address, email, user_type):
    """
    Creates a user with the specified details.
    """
    if not school_id:
      raise ValueError('Users must have a school ID')
    if not email:
      raise ValueError('Users must have an email address')

    salt = secrets.token_hex(8)  # Generate random salt
    password = school_id + salt

    user = self.model(
      school_id=school_id,
      first_name=first_name,
      surname=surname,
      address=address,
      email=self.normalize_email(email),
      user_type=user_type,
      password=self.make_password(password)
    )
    user.save(using=self._db)
    return user

  def create_superuser(self, school_id, first_name, surname, address, email):
    """
    Creates a superuser with the specified details.
    """
    user = self.create_user(school_id, first_name, surname, address, email, 'admin')
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

class User(AbstractUser):
  """
  Custom User model with   
 additional fields.
  """
  USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('admin', 'School Admin'),
  )
  user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='student')

  school_id = models.PositiveIntegerField(unique=True)
  first_name = models.CharField(max_length=50)
  surname = models.CharField(max_length=50, blank=True, null=True)
  address = models.TextField()
  email = models.EmailField(unique=True)

  USERNAME_FIELD = 'school_id'  # Use school ID for authentication
  REQUIRED_FIELDS = []  # No additional required fields

  objects = MyUserManager()

  def __str__(self):
    return f"{self.school_id} - {self.first_name} {self.surname}"

class Department(models.Model):
  name = models.CharField(max_length=100)

class Course(models.Model):
  name = models.CharField(max_length=100)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)   


class Student(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)   

  enrolled_course = models.ForeignKey(Course, on_delete=models.CASCADE)
  year_level = models.PositiveIntegerField()
  year_last_enrolled = models.PositiveIntegerField()