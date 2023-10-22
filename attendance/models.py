# In attendance/models.py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username

class Unit(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='units')

    def __str__(self):
        return self.name
    
    
class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    week = models.IntegerField()
    is_present = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student} - {self.unit}"
