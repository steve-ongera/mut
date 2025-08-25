# attendance/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with email login"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with email login"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="student")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "user_type"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"


# Academic Structure Models
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    dean = models.OneToOneField('Lecturer', on_delete=models.SET_NULL, null=True, blank=True, related_name='dean_of')
    established_date = models.DateField()
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Faculties"
        
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    head = models.OneToOneField('Lecturer', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.faculty.name}"

class Course(models.Model):
    COURSE_LEVELS = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('degree', 'Degree'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ]
    
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=20, choices=COURSE_LEVELS)
    duration_years = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    credit_hours = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

# User Profile Models
class Student(models.Model):
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
        (5, 'Fifth Year'),
        (6, 'Sixth Year'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
        ('transferred', 'Transferred'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    student_id = models.CharField(max_length=15, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    year_of_study = models.IntegerField(choices=YEAR_CHOICES)
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    admission_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    def get_current_gpa(self):
        """Calculate current GPA based on grades"""
        grades = self.grades.filter(is_final=True)
        if not grades.exists():
            return 0.0
        
        total_points = sum(grade.get_grade_points() * grade.unit.credit_hours for grade in grades)
        total_credits = sum(grade.unit.credit_hours for grade in grades)
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

class Lecturer(models.Model):
    RANK_CHOICES = [
        ('assistant_lecturer', 'Assistant Lecturer'),
        ('lecturer', 'Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('associate_professor', 'Associate Professor'),
        ('professor', 'Professor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('retired', 'Retired'),
        ('terminated', 'Terminated'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lecturers')
    rank = models.CharField(max_length=25, choices=RANK_CHOICES)
    hire_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    phone_number = models.CharField(max_length=15, blank=True)
    office_number = models.CharField(max_length=10, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()

# Academic Content Models
class Unit(models.Model):
    UNIT_TYPES = [
        ('core', 'Core Unit'),
        ('elective', 'Elective Unit'),
        ('project', 'Project'),
    ]
    
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='units_taught')
    students = models.ManyToManyField(Student, through='Enrollment', related_name='units')
    credit_hours = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    year_offered = models.IntegerField(choices=Student.YEAR_CHOICES)
    semester_offered = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    unit_type = models.CharField(max_length=15, choices=UNIT_TYPES, default='core')
    description = models.TextField(blank=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_enrolled_students_count(self):
        return self.students.filter(status='active').count()

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=9)  # e.g., "2023/2024"
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    enrollment_date = models.DateTimeField(default=timezone.now)
    is_retake = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'unit', 'academic_year', 'semester']
    
    def __str__(self):
        return f"{self.student} enrolled in {self.unit}"

# Assessment Models
class AssessmentType(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Assignment", "CAT", "Exam"
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage weight
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.weight}%)"

class Assessment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='assessments')
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    max_marks = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    academic_year = models.CharField(max_length=9)
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    
    def __str__(self):
        return f"{self.unit.code} - {self.title}"

class Grade(models.Model):
    LETTER_GRADES = [
        ('A', 'A (70-100)'),
        ('B', 'B (60-69)'),
        ('C', 'C (50-59)'),
        ('D', 'D (40-49)'),
        ('F', 'F (0-39)'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='grades')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2)
    letter_grade = models.CharField(max_length=2, choices=LETTER_GRADES)
    academic_year = models.CharField(max_length=9)
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    is_final = models.BooleanField(default=False)  # True for final unit grade
    graded_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    date_graded = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['student', 'unit', 'academic_year', 'semester', 'assessment']
    
    def __str__(self):
        return f"{self.student} - {self.unit.code}: {self.letter_grade}"
    
    def get_grade_points(self):
        """Convert letter grade to grade points for GPA calculation"""
        grade_points = {
            'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'I': 0.0, 'W': 0.0
        }
        return grade_points.get(self.letter_grade, 0.0)

# Attendance Models (Enhanced from your existing)
class AttendanceSession(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='attendance_sessions')
    date = models.DateTimeField()
    week_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    session_type = models.CharField(max_length=20, choices=[
        ('lecture', 'Lecture'),
        ('tutorial', 'Tutorial'),
        ('practical', 'Practical'),
        ('seminar', 'Seminar'),
    ], default='lecture')
    topic = models.CharField(max_length=200, blank=True)
    duration_minutes = models.IntegerField(default=90)
    conducted_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.unit.code} - Week {self.week_number} ({self.session_type})"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='attendance_records')
    is_present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(default=timezone.now)
    marked_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE , blank=True, null=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'session']
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} - {self.session.unit.code} Week {self.session.week_number}: {status}"

# Academic Calendar Models
class AcademicYear(models.Model):
    name = models.CharField(max_length=9, unique=True)  # e.g., "2023/2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one academic year is active at a time
            AcademicYear.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class Semester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    number = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateField()
    is_active = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['academic_year', 'number']
    
    def __str__(self):
        return f"{self.academic_year.name} - Semester {self.number}"

# Fee Management Models
class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2')])
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    activity_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['course', 'academic_year', 'semester']
    
    def __str__(self):
        return f"{self.course.code} - {self.academic_year.name} S{self.semester}"
    
    @property
    def total_fee(self):
        return self.tuition_fee + self.activity_fee + self.library_fee + self.lab_fee + self.other_fees

class FeePayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('mobile', 'Mobile Money'),
        ('card', 'Card Payment'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=50, unique=True)
    receipt_number = models.CharField(max_length=20, unique=True, blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    def __str__(self):
        return f"{self.student} - {self.amount_paid} ({self.payment_date.date()})"
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"RCP{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)

# Library Models
class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    opening_hours = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Libraries"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    category = models.CharField(max_length=50)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    @property
    def is_available(self):
        return self.available_copies > 0

class BookBorrowing(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} borrowed {self.book.title}"
    
    @property
    def is_overdue(self):
        return not self.is_returned and timezone.now() > self.due_date
    
    def calculate_fine(self):
        """Calculate fine for overdue books"""
        if self.is_overdue:
            days_overdue = (timezone.now() - self.due_date).days
            fine_per_day = 10  # KES 10 per day
            return days_overdue * fine_per_day
        return 0