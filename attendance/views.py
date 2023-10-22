
# In attendance/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, AttendanceRecord
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('check_in')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def check_in(request):
    student = request.user.student
    today = timezone.now().date()
    # Check if the student has already checked in for today
    if not AttendanceRecord.objects.filter(student=student, date=today).exists():
        AttendanceRecord.objects.create(student=student, date=today)
    return redirect('view_attendance')

@login_required
def view_attendance(request):
    student = request.user.student
    attendance_records = AttendanceRecord.objects.filter(student=student)
    return render(request, 'view_attendance.html', {'attendance_records': attendance_records})

# Create your views here.
def home(request):
    return render(request, "home.html")