from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, StudentRegistrationForm

def login_view(request):
  """
  Handles user login requests.
  """
  if request.method == 'POST':
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
      school_id = login_form.cleaned_data['school_id']
      password = login_form.cleaned_data['password']
      user = authenticate(school_id=school_id, password=password)
      if user is not None:
        login(request, user)
        return redirect('home')  # Replace 'home' with your desired redirect URL
      else:
        # Login failed
        error_message = "Invalid school ID or password."
        context = {'error_message': error_message, 'login_form': login_form}
        return render(request, 'login.html', context)
  else:
    login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)

def register_view(request):
  """
  Handles user registration requests.
  """
  if request.method == 'POST':
    if 'user_type' in request.POST and request.POST['user_type'] == 'student':
      # Student registration
      register_form = StudentRegistrationForm(request.POST)
    else:
      # Other user types (instructor, admin)
      register_form = UserRegistrationForm(request.POST)
    if register_form.is_valid():
      register_form.save()  # Saves user and related data
      return redirect('login')  # Replace 'login' with your desired redirect URL
    else:
      # Registration failed
      context = {'register_form': register_form}
      return render(request, 'register.html', context)
  else:
    # User type selection on initial GET request
    user_type_choices = User.USER_TYPE_CHOICES
    context = {'user_type_choices': user_type_choices}
    return render(request, 'register_type.html', context)

def home_view(request):
  """
  Home page view.
  """
  return render(request, 'home.html')

def logout_view(request):
  """
  Logs out the user.
  """
  logout(request)
  return redirect('login')  # Replace 'login' with your desired redirect URL