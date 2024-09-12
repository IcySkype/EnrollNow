from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Department, Course

class UserRegistrationForm(UserCreationForm):
  """
  Form for user registration (students, instructors, admins).
  """
  first_name = forms.CharField(max_length=50)
  surname = forms.CharField(max_length=50, required=False)
  address = forms.CharField(widget=forms.Textarea)
  email = forms.EmailField()
  department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)

  class Meta(UserCreationForm.Meta):
    model = User
    fields = ['school_id', 'first_name', 'surname', 'address', 'email', 'user_type']

class StudentRegistrationForm(UserRegistrationForm):
  """
  Form for student registration with additional fields.
  """
  enrolled_course = forms.ModelChoiceField(queryset=Course.objects.all())
  year_level = forms.IntegerField(min_value=1)
  year_last_enrolled = forms.IntegerField()

  class Meta:
    model = User
    fields = UserRegistrationForm.Meta.fields + ['department', 'enrolled_course', 'year_level', 'year_last_enrolled']

class LoginForm(forms.Form):
  """
  Form for user login.
  """
  school_id = forms.CharField(max_length=5)
  password = forms.CharField(widget=forms.PasswordInput)

  def clean_school_id(self):
    """
    Validates school ID format.
    """
    school_id = self.cleaned_data['school_id']
    if not school_id.isdigit() or len(school_id) != 5:
      raise forms.ValidationError("Invalid school ID format. Please enter a 5-digit number.")
    return school_id