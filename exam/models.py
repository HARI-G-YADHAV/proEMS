print("Loading models...")
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exam(models.Model):
    sem = models.IntegerField()
    year = models.IntegerField()
    month = models.CharField(max_length=20)
    grad_level = models.CharField(max_length=20)
    date = models.DateField(default="2020-01-01")

    def __str__(self):      
        return self.grad_level

class Department(models.Model):
    dept_id = models.IntegerField(primary_key=True)
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name


class Programme(models.Model):
    pgm_id = models.IntegerField(unique=True)
    pgm_name = models.CharField(max_length=50)
    grad_level = models.ForeignKey(Exam,on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.pgm_name

class Course(models.Model):
    course_id = models.IntegerField()
    course_title = models.CharField(max_length=50)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE)
    syllabus_year = models.IntegerField()
    course_code= models.CharField(max_length=20)
    grad_level = models.CharField(max_length=2, default="UG")
    semester = models.IntegerField()
    lab_theory = models.CharField(max_length=2, default="T")
                                  
    def __str__(self):
        return self.course_title

class ExamTimeTable(models.Model):
    #exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,models.CASCADE)
    dept=models.ForeignKey(Department,on_delete=models.CASCADE)
    date=models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    #grad_level = models.CharField(max_length=2, default="UG")
    semester = models.IntegerField()

    def __str__(self):
        return self.course_id.course_title


class teacherTable(models.Model):
    teacher_id = models.IntegerField()
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class room(models.Model):
    room_id=models.IntegerField()
    room_no=models.IntegerField()
    no_of_coloums=models.IntegerField()
    location=models.CharField(max_length=40)

    def __str__(self):
        return str(self.room_id)


    

class preferTable(models.Model):
    teacher_id = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    course_id = models.ForeignKey(ExamTimeTable,default=1, on_delete=models.CASCADE)
    date=models.DateField()


class Timetable(models.Model):
    exam_id=models.IntegerField()
    date=models.DateField()
    course_id=models.IntegerField()


class dutyAllotment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    course_id = models.ForeignKey(ExamTimeTable, on_delete=models.CASCADE)
    date = models.DateField()
    room_id = models.ForeignKey(room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.course_id} on {self.date}"
