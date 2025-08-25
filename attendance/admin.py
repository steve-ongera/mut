# attendance/admin.py
from django.contrib import admin
from django.db.models import Count, Avg
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
import datetime

from .models import (
    Faculty, Department, Course, Student, Lecturer, Unit, Enrollment,
    AssessmentType, Assessment, Grade, AttendanceSession, AttendanceRecord,
    AcademicYear, Semester, FeeStructure, FeePayment, Library, Book, BookBorrowing
)

# Inline classes for better organization
class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    fields = ('name', 'code', 'head')
    readonly_fields = ('head',)

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    fields = ('code', 'name', 'credit_hours', 'year_offered', 'semester_offered')
    readonly_fields = ('code',)

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    fields = ('unit', 'academic_year', 'semester', 'is_retake')

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0
    fields = ('unit', 'assessment', 'marks', 'letter_grade', 'is_final')
    readonly_fields = ('unit', 'assessment')

class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0
    fields = ('session', 'is_present', 'marked_at', 'notes')
    readonly_fields = ('marked_at',)

class FeePaymentInline(admin.TabularInline):
    model = FeePayment
    extra = 0
    fields = ('fee_structure', 'amount_paid', 'payment_date', 'payment_method', 'verified')
    readonly_fields = ('payment_date', 'receipt_number')

class AssessmentInline(admin.TabularInline):
    model = Assessment
    extra = 0
    fields = ('title', 'assessment_type', 'due_date', 'max_marks')

# Main Admin Classes
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'dean', 'established_date', 'department_count')
    list_filter = ('established_date',)
    search_fields = ('name', 'code')
    inlines = [DepartmentInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'established_date')
        }),
        ('Leadership', {
            'fields': ('dean',)
        }),
        ('Details', {
            'fields': ('description',)
        }),
    )
    
    def department_count(self, obj):
        return obj.departments.count()
    department_count.short_description = 'Departments'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'faculty', 'head', 'course_count', 'lecturer_count')
    list_filter = ('faculty',)
    search_fields = ('name', 'code', 'faculty__name')
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'faculty')
        }),
        ('Leadership', {
            'fields': ('head',)
        }),
        ('Details', {
            'fields': ('description',)
        }),
    )
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Courses'
    
    def lecturer_count(self, obj):
        return obj.lecturers.count()
    lecturer_count.short_description = 'Lecturers'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'level', 'duration_years', 'credit_hours', 'student_count')
    list_filter = ('level', 'department__faculty', 'department', 'duration_years')
    search_fields = ('name', 'code', 'department__name')
    inlines = [UnitInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'department')
        }),
        ('Academic Details', {
            'fields': ('level', 'duration_years', 'credit_hours')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    
    def student_count(self, obj):
        return obj.students.filter(status='active').count()
    student_count.short_description = 'Active Students'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'course', 'year_of_study', 'semester', 'status', 'current_gpa')
    list_filter = ('course', 'year_of_study', 'semester', 'status', 'course__department')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    inlines = [EnrollmentInline, GradeInline, AttendanceRecordInline, FeePaymentInline]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'student_id')
        }),
        ('Academic Information', {
            'fields': ('course', 'year_of_study', 'semester', 'admission_date', 'graduation_date', 'status')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
    )
    
    readonly_fields = ('current_gpa',)
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'user__first_name'
    
    def current_gpa(self, obj):
        gpa = obj.get_current_gpa()
        if gpa >= 3.5:
            color = 'green'
        elif gpa >= 2.5:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}</span>', color, gpa)
    current_gpa.short_description = 'Current GPA'

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'rank', 'status', 'units_taught_count')
    list_filter = ('department', 'rank', 'status', 'department__faculty')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email', 'specialization')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'employee_id')
        }),
        ('Employment Details', {
            'fields': ('department', 'rank', 'hire_date', 'status', 'specialization')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'office_number')
        }),
    )
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'user__first_name'
    
    def units_taught_count(self, obj):
        return obj.units_taught.count()
    units_taught_count.short_description = 'Units Taught'

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course', 'lecturer', 'credit_hours', 'year_offered', 'semester_offered', 'enrolled_students')
    list_filter = ('course', 'year_offered', 'semester_offered', 'unit_type', 'course__department')
    search_fields = ('code', 'name', 'course__name', 'lecturer__user__last_name')
    filter_horizontal = ('prerequisites',)
    inlines = [AssessmentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'course', 'lecturer')
        }),
        ('Academic Details', {
            'fields': ('credit_hours', 'year_offered', 'semester_offered', 'unit_type')
        }),
        ('Prerequisites', {
            'fields': ('prerequisites',)
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    
    def enrolled_students(self, obj):
        count = obj.get_enrolled_students_count()
        url = reverse('admin:attendance_enrollment_changelist') + f'?unit__id__exact={obj.id}'
        return format_html('<a href="{}">{} students</a>', url, count)
    enrolled_students.short_description = 'Enrolled'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'unit', 'academic_year', 'semester', 'enrollment_date', 'is_retake')
    list_filter = ('academic_year', 'semester', 'is_retake', 'unit__course')
    search_fields = ('student__student_id', 'student__user__last_name', 'unit__code', 'unit__name')
    date_hierarchy = 'enrollment_date'

@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'description')
    search_fields = ('name',)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'assessment_type', 'due_date', 'max_marks', 'academic_year', 'semester')
    list_filter = ('assessment_type', 'academic_year', 'semester', 'unit__course')
    search_fields = ('title', 'unit__code', 'unit__name')
    date_hierarchy = 'due_date'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'unit', 'assessment', 'marks', 'letter_grade', 'is_final', 'graded_by', 'date_graded')
    list_filter = ('letter_grade', 'is_final', 'academic_year', 'semester', 'unit__course')
    search_fields = ('student__student_id', 'student__user__last_name', 'unit__code')
    date_hierarchy = 'date_graded'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student__user', 'unit', 'graded_by__user')

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('unit', 'date', 'week_number', 'session_type', 'topic', 'conducted_by', 'attendance_rate')
    list_filter = ('session_type', 'unit__course', 'week_number')
    search_fields = ('unit__code', 'unit__name', 'topic', 'conducted_by__user__last_name')
    date_hierarchy = 'date'
    
    def attendance_rate(self, obj):
        total_records = obj.attendance_records.count()
        if total_records == 0:
            return "No records"
        
        present_count = obj.attendance_records.filter(is_present=True).count()
        rate = (present_count / total_records) * 100
        
        if rate >= 80:
            color = 'green'
        elif rate >= 60:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html('<span style="color: {};">{:.1f}%</span>', color, rate)
    attendance_rate.short_description = 'Attendance Rate'

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session_info', 'is_present', 'marked_at', 'marked_by')
    list_filter = ('is_present', 'session__unit__course', 'session__session_type')
    search_fields = ('student__student_id', 'student__user__last_name', 'session__unit__code')
    date_hierarchy = 'marked_at'
    
    def session_info(self, obj):
        return f"{obj.session.unit.code} - Week {obj.session.week_number}"
    session_info.short_description = 'Session'

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'number', 'start_date', 'end_date', 'registration_deadline', 'is_active')
    list_filter = ('academic_year', 'number', 'is_active')
    date_hierarchy = 'start_date'

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('course', 'academic_year', 'semester', 'tuition_fee', 'total_fee')
    list_filter = ('academic_year', 'semester', 'course__department')
    search_fields = ('course__code', 'course__name')
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course', 'academic_year', 'semester')
        }),
        ('Fee Breakdown', {
            'fields': ('tuition_fee', 'activity_fee', 'library_fee', 'lab_fee', 'other_fees')
        }),
    )

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'payment_date', 'payment_method', 'reference_number', 'verified', 'verified_by')
    list_filter = ('payment_method', 'verified', 'payment_date', 'fee_structure__academic_year')
    search_fields = ('student__student_id', 'student__user__last_name', 'reference_number', 'receipt_number')
    date_hierarchy = 'payment_date'
    readonly_fields = ('receipt_number',)
    
    actions = ['mark_as_verified', 'mark_as_unverified']
    
    def mark_as_verified(self, request, queryset):
        queryset.update(verified=True, verified_by=request.user)
        self.message_user(request, f"{queryset.count()} payments marked as verified.")
    mark_as_verified.short_description = "Mark selected payments as verified"
    
    def mark_as_unverified(self, request, queryset):
        queryset.update(verified=False, verified_by=None)
        self.message_user(request, f"{queryset.count()} payments marked as unverified.")
    mark_as_unverified.short_description = "Mark selected payments as unverified"

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'opening_hours', 'book_count')
    search_fields = ('name', 'location')
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Total Books'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'library', 'total_copies', 'available_copies', 'availability_status')
    list_filter = ('category', 'library', 'publication_year')
    search_fields = ('title', 'author', 'isbn', 'publisher')
    
    def availability_status(self, obj):
        if obj.is_available:
            return format_html('<span style="color: green;">Available</span>')
        else:
            return format_html('<span style="color: red;">Not Available</span>')
    availability_status.short_description = 'Status'

@admin.register(BookBorrowing)
class BookBorrowingAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'due_date', 'return_date', 'is_returned', 'overdue_status', 'fine_amount')
    list_filter = ('is_returned', 'borrow_date', 'due_date')
    search_fields = ('student__student_id', 'student__user__last_name', 'book__title')
    date_hierarchy = 'borrow_date'
    
    actions = ['mark_as_returned']
    
    def overdue_status(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Overdue</span>')
        elif obj.is_returned:
            return format_html('<span style="color: green;">Returned</span>')
        else:
            return format_html('<span style="color: blue;">On Loan</span>')
    overdue_status.short_description = 'Status'
    
    def mark_as_returned(self, request, queryset):
        for borrowing in queryset:
            if not borrowing.is_returned:
                borrowing.is_returned = True
                borrowing.return_date = datetime.datetime.now()
                borrowing.fine_amount = borrowing.calculate_fine()
                borrowing.save()
                
                # Update book availability
                book = borrowing.book
                book.available_copies += 1
                book.save()
        
        self.message_user(request, f"{queryset.count()} books marked as returned.")
    mark_as_returned.short_description = "Mark selected books as returned"

# Customize admin site headers
admin.site.site_header = "Muranga University Administration"
admin.site.site_title = "Muranga University Admin"
admin.site.index_title = "University Management System"