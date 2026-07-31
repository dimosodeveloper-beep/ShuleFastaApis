from django.db import models
from django.contrib.auth.models import AbstractUser




class School(models.Model):
    name = models.CharField(max_length=255)
    name_SW = models.CharField(max_length=255, blank=True, null=True)

    location = models.CharField(max_length=255)
    location_SW = models.CharField(max_length=255, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('owner', 'Owner'),
    )

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='teacher'
    )

    role_SW = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username



class AcademicYear(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    year = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.year)




class ClassRoom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    name_SW = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.name} - {self.name}"


class Stream(models.Model):
    name = models.CharField(max_length=50)
    name_SW = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    classroom = models.ForeignKey(
        ClassRoom,
        related_name="streams",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    name_SW = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# 🔥 HAPA NDIO MUHIMU (Student bila class)
class Student(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    parent = models.ForeignKey(
        CustomerUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )

    first_name = models.CharField(max_length=100)
    first_name_SW = models.CharField(max_length=100, blank=True, null=True)

    last_name = models.CharField(max_length=100)
    last_name_SW = models.CharField(max_length=100, blank=True, null=True)

    admission_number = models.CharField(max_length=50)
    admission_number_SW = models.CharField(max_length=50, blank=True, null=True)

    gender = models.CharField(max_length=10)
    gender_SW = models.CharField(max_length=10, blank=True, null=True)

    student_health = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# 🔥 HISTORY YA MWANAFUNZI
class StudentEnrollment(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE
    )

    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE
    )

    year = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.classroom} - {self.year}"


class Teacher(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    user = models.OneToOneField(
        CustomerUser,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=20)
    phone_SW = models.CharField(max_length=20, blank=True, null=True)

    subject = models.ManyToManyField(Subject, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class FeeStructure(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    amount = models.FloatField()

    term = models.CharField(max_length=50)
    term_SW = models.CharField(max_length=50, blank=True, null=True)

    year = models.IntegerField()

    def __str__(self):
        return f"{self.classroom.name} - {self.amount}"


class FeePayment(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    amount_paid = models.FloatField()
    payment_date = models.DateField()

    term = models.CharField(max_length=50)
    term_SW = models.CharField(max_length=50, blank=True, null=True)

    year = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.amount_paid}"


class ExamCategory(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    name_SW = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Exam(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    classrooms = models.ManyToManyField(ClassRoom)

    category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    name_SW = models.CharField(max_length=100, blank=True, null=True)

    date = models.DateField()

    def __str__(self):
        return self.name


# 🔥 RESULT SASA INA YEAR + CLASS
class Result(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    year = models.IntegerField()

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    marks = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)

    grade = models.CharField(max_length=50, blank=True, null=True)
    grade_SW = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.marks}"


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    year = models.IntegerField()

    date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    status_SW = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)

    reason = models.TextField(blank=True, null=True)
    reason_SW = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date}"


class Timetable(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    day = models.CharField(max_length=20)
    day_SW = models.CharField(max_length=20, blank=True, null=True)

    start_time = models.TimeField()
    end_time = models.TimeField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classroom} - {self.stream} - {self.subject} - {self.day}"


class GradingSystem(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    grade = models.CharField(max_length=2)
    grade_SW = models.CharField(max_length=2, blank=True, null=True)

    min_score = models.IntegerField()
    max_score = models.IntegerField()

    remark = models.CharField(max_length=50)
    remark_SW = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.grade} ({self.min_score}-{self.max_score})"


class SchoolEvent(models.Model):

    EVENT_TYPE = (
        ('exam', 'Exam'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('activity', 'Activity'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    title_SW = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    description_SW = models.TextField(blank=True, null=True)

    event_type = models.CharField(max_length=20, choices=EVENT_TYPE)
    event_type_SW = models.CharField(max_length=20, choices=EVENT_TYPE, blank=True, null=True)

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


class StudentBehaviour(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    title_SW = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField()
    description_SW = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=100)
    status_SW = models.CharField(max_length=100, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.title}"





class ParentComment(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    parent = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    comment = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent.username} - {self.school.name}"


class TeacherScheme(models.Model):

    TERM_CHOICES = (
        ("term1", "Term 1"),
        ("term2", "Term 2"),
        ("term3", "Term 3"),
        ("term4", "Term 4"),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    term = models.CharField(max_length=20, choices=TERM_CHOICES)

    topic = models.CharField(max_length=255)
    content = models.TextField()

    week = models.IntegerField()

    # 🔥 NEW FIELDS
    from_date = models.DateField()
    to_date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher} - {self.term}"




class PasswordResetOTP(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"