from django.db import models
from django.contrib.auth.models import AbstractUser


class School(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return self.username


class ClassRoom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.name} - {self.name}"


# class Stream(models.Model):
#     classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.classroom.name} {self.name}"


class Stream(models.Model):
    name = models.CharField(max_length=50)
    classroom = models.ForeignKey(
        ClassRoom,
        related_name="streams",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name




class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Subject(models.Model):
#     school = models.ForeignKey(School, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     classrooms = models.ManyToManyField(ClassRoom, blank=True, related_name="subjects")
#     streams = models.ManyToManyField(Stream, blank=True, related_name="subjects")

#     def __str__(self):
#         return self.name

class Student(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    # Ongeza field hii kwenye Student model ili mwanafunzi awe na mzazi.
    parent = models.ForeignKey(
    CustomerUser,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="children"
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    admission_number = models.CharField(max_length=50)

    gender = models.CharField(max_length=10)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

##############################################################


# Sawa, sasa tunaendelea na STEP 6: Teacher Management + Fee Management + School Dashboard Analytics kwa kutumia Django REST Framework.
# Hatua hii itafanya mfumo wako uwe karibu kabisa na School ERP kamili.

# Modules tutakazoongeza:

# 1️⃣ Teacher Management System
# 2️⃣ Student Fee Management System
# 3️⃣ School Dashboard Statistics APIs

# models.py (ADD TEACHER + FEES MODELS – FULL CODE)

# Ongeza models hizi chini ya Student model.

# class Teacher(models.Model):

#     school = models.ForeignKey(School, on_delete=models.CASCADE)

#     user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)

#     phone = models.CharField(max_length=20)

#     subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

class Teacher(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20)

    subject = models.ManyToManyField(Subject, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class FeeStructure(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    amount = models.FloatField()

    term = models.CharField(max_length=50)

    year = models.IntegerField()

    def __str__(self):
        return f"{self.classroom.name} - {self.amount}"


class FeePayment(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    amount_paid = models.FloatField()

    payment_date = models.DateField()

    term = models.CharField(max_length=50)

    year = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.amount_paid}"



# Sawa, sasa tunaendelea na STEP 2: Professional Exam + Results System kwa kutumia Django REST Framework.
# Hatua hii itaongeza uwezo wa mfumo wako kufanya:

# Kuunda Exam Categories (Daily Test, Midterm, Terminal n.k.)

# Kuunda Exam

# Kuongeza Subjects

# Kuongeza Results

# Bulk upload results

# Kuona results za mwanafunzi

# Kuona results za exam fulani


class ExamCategory(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Exam(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    classrooms = models.ManyToManyField(ClassRoom)  # 🔥 BADILIKO HAPA

    category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    date = models.DateField()

    def __str__(self):
        return self.name

class Result(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    marks = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)

    grade = models.CharField(max_length=50, blank=True, null=True)  # ✅ ONGEZA HII

    def __str__(self):
        return f"{self.student} - {self.marks}"





####################  ATTENDANCE ##############################

# class Attendance(models.Model):

#     STATUS_CHOICES = (
#         ('present', 'Present'),
#         ('absent', 'Absent'),
#     )

#     school = models.ForeignKey(School, on_delete=models.CASCADE)

#     student = models.ForeignKey(Student, on_delete=models.CASCADE)

#     classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

#     stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

#     date = models.DateField()

#     status = models.CharField(max_length=10, choices=STATUS_CHOICES)

#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('student', 'date')

#     def __str__(self):
#         return f"{self.student} - {self.date}"



class Attendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reason = models.TextField(blank=True, null=True)  # <=== NEW FIELD

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date}"



# Sasa tunaendelea na STEP 7: Timetable System + Grading System + PDF Report Cards kwa kutumia Django REST Framework.
# Hatua hii itafanya mfumo wako uwe School ERP ya professional kabisa kama mifumo inayotumiwa na shule nyingi.

# Modules mpya:

# 1️⃣ Timetable System (Ratiba ya Vipindi)
# 2️⃣ Grading System (A, B, C, D, F)
# 3️⃣ Automatic PDF Report Card Generator

# 1. Timetable System
# models.py (ADD TIMETABLE MODEL)

# class Timetable(models.Model):

#     school = models.ForeignKey(School, on_delete=models.CASCADE)

#     classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

#     day = models.CharField(max_length=20)

#     start_time = models.TimeField()

#     end_time = models.TimeField()

#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.classroom} - {self.subject} - {self.day}"


class Timetable(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)  # ✅ NEW FIELD

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    day = models.CharField(max_length=20)

    start_time = models.TimeField()

    end_time = models.TimeField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classroom} - {self.stream} - {self.subject} - {self.day}"








# Grading System
# models.py (ADD GRADING MODEL)

class GradingSystem(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    grade = models.CharField(max_length=2)

    min_score = models.IntegerField()

    max_score = models.IntegerField()

    remark = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.grade} ({self.min_score}-{self.max_score})"










#################  CALENDER

class SchoolEvent(models.Model):

    EVENT_TYPE = (
        ('exam', 'Exam'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('activity', 'Activity'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, null=True)

    event_type = models.CharField(max_length=20, choices=EVENT_TYPE)

    start_date = models.DateField()

    end_date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_date})"




class ReportSent(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report sent: {self.student} - {self.exam.name}"
















