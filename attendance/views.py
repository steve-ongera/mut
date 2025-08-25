# attendance/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    CustomUser, Student, Lecturer, Unit, AttendanceSession, 
    AttendanceRecord, Course, Department, Faculty, Enrollment,
    Grade, AcademicYear, Semester, FeePayment, Book, BookBorrowing
)


def login_view(request):
    """Handle login for different user types and redirect to appropriate dashboard"""
    if request.user.is_authenticated:
        return redirect_to_dashboard(request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.full_name}!')
                    return redirect_to_dashboard(user)
                else:
                    messages.error(request, 'Your account is inactive. Please contact admin.')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please provide both email and password.')
    
    return render(request, 'auth/login.html')


def redirect_to_dashboard(user):
    """Redirect user to appropriate dashboard based on user type"""
    if user.user_type == 'admin' or user.is_superuser:
        return redirect('admin_dashboard')
    elif user.user_type == 'teacher':
        return redirect('teacher_dashboard')
    elif user.user_type == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('login')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def admin_dashboard(request):
    """Admin dashboard with system overview"""
    # Check if user is admin
    if request.user.user_type != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('login')
    
    # Get statistics
    total_students = Student.objects.filter(status='active').count()
    total_lecturers = Lecturer.objects.filter(status='active').count()
    total_courses = Course.objects.count()
    total_units = Unit.objects.count()
    total_faculties = Faculty.objects.count()
    total_departments = Department.objects.count()
    
    # Recent enrollments (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_enrollments = Enrollment.objects.filter(
        enrollment_date__gte=thirty_days_ago
    ).count()
    
    # Attendance statistics
    current_academic_year = AcademicYear.objects.filter(is_active=True).first()
    if current_academic_year:
        total_sessions = AttendanceSession.objects.filter(
            date__year=timezone.now().year
        ).count()
        
        attendance_rate = AttendanceRecord.objects.filter(
            session__date__year=timezone.now().year,
            is_present=True
        ).count()
        
        total_attendance_records = AttendanceRecord.objects.filter(
            session__date__year=timezone.now().year
        ).count()
        
        attendance_percentage = (
            (attendance_rate / total_attendance_records) * 100 
            if total_attendance_records > 0 else 0
        )
    else:
        total_sessions = 0
        attendance_percentage = 0
    
    # Recent students (last 10)
    recent_students = Student.objects.select_related('user', 'course').order_by('-admission_date')[:10]
    
    # Recent lecturers (last 10)
    recent_lecturers = Lecturer.objects.select_related('user', 'department').order_by('-hire_date')[:10]
    
    # Fee payment statistics
    current_year = timezone.now().year
    total_fees_paid = FeePayment.objects.filter(
        payment_date__year=current_year,
        verified=True
    ).aggregate(total=models.Sum('amount_paid'))['total'] or 0
    
    context = {
        'total_students': total_students,
        'total_lecturers': total_lecturers,
        'total_courses': total_courses,
        'total_units': total_units,
        'total_faculties': total_faculties,
        'total_departments': total_departments,
        'recent_enrollments': recent_enrollments,
        'total_sessions': total_sessions,
        'attendance_percentage': round(attendance_percentage, 2),
        'recent_students': recent_students,
        'recent_lecturers': recent_lecturers,
        'total_fees_paid': total_fees_paid,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    """Teacher dashboard with teaching-related information"""
    # Check if user is teacher
    if request.user.user_type != 'teacher':
        messages.error(request, 'Access denied. Teacher privileges required.')
        return redirect('login')
    
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        messages.error(request, 'Lecturer profile not found. Please contact admin.')
        return redirect('login')
    
    # Get units taught by this lecturer
    units_taught = Unit.objects.filter(lecturer=lecturer).prefetch_related('students')
    
    # Get total students taught
    total_students = 0
    for unit in units_taught:
        total_students += unit.students.filter(status='active').count()
    
    # Get recent attendance sessions
    recent_sessions = AttendanceSession.objects.filter(
        conducted_by=lecturer
    ).order_by('-date')[:10]
    
    # Get attendance statistics for units taught
    current_week = timezone.now().isocalendar()[1]
    weekly_sessions = AttendanceSession.objects.filter(
        conducted_by=lecturer,
        date__week=current_week
    ).count()
    
    # Calculate average attendance rate for lecturer's units
    lecturer_attendance_records = AttendanceRecord.objects.filter(
        session__conducted_by=lecturer,
        session__date__month=timezone.now().month
    )
    
    total_records = lecturer_attendance_records.count()
    present_records = lecturer_attendance_records.filter(is_present=True).count()
    attendance_rate = (present_records / total_records * 100) if total_records > 0 else 0
    
    # Get students with low attendance in lecturer's units
    low_attendance_students = []
    for unit in units_taught:
        unit_sessions = AttendanceSession.objects.filter(unit=unit).count()
        if unit_sessions > 0:
            for student in unit.students.filter(status='active'):
                present_count = AttendanceRecord.objects.filter(
                    student=student,
                    session__unit=unit,
                    is_present=True
                ).count()
                attendance_percentage = (present_count / unit_sessions) * 100
                if attendance_percentage < 75:  # Below 75% attendance
                    low_attendance_students.append({
                        'student': student,
                        'unit': unit,
                        'attendance_percentage': round(attendance_percentage, 2)
                    })
    
    # Get grades to be entered (recent assessments without grades)
    pending_grades = Grade.objects.filter(
        graded_by=lecturer,
        marks__isnull=True
    ).select_related('student', 'unit', 'assessment')[:10]
    
    context = {
        'lecturer': lecturer,
        'units_taught': units_taught,
        'total_units': units_taught.count(),
        'total_students': total_students,
        'recent_sessions': recent_sessions,
        'weekly_sessions': weekly_sessions,
        'attendance_rate': round(attendance_rate, 2),
        'low_attendance_students': low_attendance_students[:10],
        'pending_grades': pending_grades,
    }
    
    return render(request, 'teacher/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    """Student dashboard with academic information"""
    # Check if user is student
    if request.user.user_type != 'student':
        messages.error(request, 'Access denied. Student privileges required.')
        return redirect('login')
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact admin.')
        return redirect('login')
    
    # Get current academic year and semester
    current_academic_year = AcademicYear.objects.filter(is_active=True).first()
    current_semester = Semester.objects.filter(is_active=True).first()
    
    # Get current enrollments
    current_enrollments = Enrollment.objects.filter(
        student=student,
        academic_year=current_academic_year.name if current_academic_year else timezone.now().year
    ).select_related('unit', 'unit__lecturer')
    
    # Calculate attendance for each enrolled unit
    units_attendance = []
    for enrollment in current_enrollments:
        unit = enrollment.unit
        total_sessions = AttendanceSession.objects.filter(unit=unit).count()
        attended_sessions = AttendanceRecord.objects.filter(
            student=student,
            session__unit=unit,
            is_present=True
        ).count()
        
        attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        units_attendance.append({
            'unit': unit,
            'total_sessions': total_sessions,
            'attended_sessions': attended_sessions,
            'attendance_percentage': round(attendance_percentage, 2)
        })
    
    # Get recent grades
    recent_grades = Grade.objects.filter(
        student=student
    ).select_related('unit', 'assessment').order_by('-date_graded')[:10]
    
    # Calculate current GPA
    current_gpa = student.get_current_gpa()
    
    # Get fee payment information
    if current_academic_year and current_semester:
        fee_payments = FeePayment.objects.filter(
            student=student,
            fee_structure__academic_year=current_academic_year
        ).order_by('-payment_date')
        
        total_paid = sum(payment.amount_paid for payment in fee_payments if payment.verified)
    else:
        fee_payments = []
        total_paid = 0
    
    # Get borrowed books
    borrowed_books = BookBorrowing.objects.filter(
        student=student,
        is_returned=False
    ).select_related('book')
    
    overdue_books = [book for book in borrowed_books if book.is_overdue]
    
    # Get upcoming sessions (next 7 days)
    next_week = timezone.now() + timedelta(days=7)
    upcoming_sessions = AttendanceSession.objects.filter(
        unit__in=[enrollment.unit for enrollment in current_enrollments],
        date__range=[timezone.now(), next_week]
    ).order_by('date')
    
    context = {
        'student': student,
        'current_academic_year': current_academic_year,
        'current_semester': current_semester,
        'units_attendance': units_attendance,
        'recent_grades': recent_grades,
        'current_gpa': current_gpa,
        'fee_payments': fee_payments[:5],  # Last 5 payments
        'total_paid': total_paid,
        'borrowed_books': borrowed_books,
        'overdue_books': overdue_books,
        'upcoming_sessions': upcoming_sessions[:5],
        'total_units': current_enrollments.count(),
    }
    
    return render(request, 'student/student_dashboard.html', context)