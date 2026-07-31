from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from deep_translator import GoogleTranslator

class AcademicYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicYear
        fields = "__all__"

class DashboardStatsSerializer(serializers.Serializer):
    results_count = serializers.IntegerField()
    attendance_count = serializers.IntegerField()
    exams_count = serializers.IntegerField()
    students_count = serializers.IntegerField()


class UserDataSerializer(serializers.ModelSerializer):
    #JinaLaKituo = VituoVyoteSerializer(many=False)

    class Meta:
        model = CustomerUser
        fields = '__all__'
        # fields = ['id', 'username', 'email','phone','first_name','profile_image']



class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"





class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerUser
        fields = [
            'id',
            'username',
            'password',
            'confirm_password',
            'email',
            'role',
            'school'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'school': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        user = CustomerUser.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
            role=validated_data.get('role'),
            school=validated_data.get('school')
        )



class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = "__all__"

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = "__all__"


# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"

    def create(self, validated_data):

        name = validated_data.get("name")

        if name:
            validated_data["name_SW"] = GoogleTranslator(
                source='en',
                target='sw'
            ).translate(name)

        return super().create(validated_data)
# class StreamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stream
#         fields = ["id","name"]


class ClassRoomSubjectSerializer(serializers.ModelSerializer):

    streams = StreamSerializer(many=True, read_only=True)

    class Meta:
        model = ClassRoom
        fields = ["id", "name", "streams"]


# class SubjectSerializer(serializers.ModelSerializer):

#     classrooms = serializers.PrimaryKeyRelatedField(
#         queryset=ClassRoom.objects.all(),
#         many=True,
#         required=False
#     )

#     streams = serializers.PrimaryKeyRelatedField(
#         queryset=Stream.objects.all(),
#         many=True,
#         required=False
#     )

#     class Meta:
#         model = Subject
#         fields = ["id", "name", "school", "classrooms", "streams"]
#         read_only_fields = ["school"]





class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"





#####################################################################


class ExamCategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = ExamCategory
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    #classroom=ClassRoomSerializer(many=False)
    school=SchoolSerializer(many=False)
    category=ExamCategorySerializer(many=False)

    class Meta:
        model = Exam
        fields = "__all__"

class CreateExamSerializer(serializers.ModelSerializer):

    classrooms = serializers.PrimaryKeyRelatedField(
        queryset=ClassRoom.objects.all(),
        many=True
    )

    class Meta:
        model = Exam
        fields = "__all__"
        read_only_fields = ["school"]

    def create(self, validated_data):
        classrooms = validated_data.pop('classrooms')
        school = self.context['request'].user.school   # 🔥 HAPA NDIO FIX

        exam = Exam.objects.create(
            school=school,   # 🔥 WEKA HAPA
            **validated_data
        )

        exam.classrooms.set(classrooms)
        return exam


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"

class CreateResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"

class CreateAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"


class StudentPromotionSerializer(serializers.Serializer):

    student = serializers.IntegerField()

    new_classroom = serializers.IntegerField()

    new_stream = serializers.IntegerField()





# class TeacherSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Teacher
#         fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username", read_only=True)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = "__all__"

    def get_subjects(self, obj):
        return [
            {
                "id": sub.id,
                "name": sub.name
            }
            for sub in obj.subject.all()
        ]


# class FeeStructureSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = FeeStructure
#         fields = "__all__"


# class FeePaymentSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = FeePayment
#         fields = "__all__"

from rest_framework import serializers
from .models import *
from django.db.models import Sum


class FeeStructureSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(
        source="classroom.name",
        read_only=True
    )

    class Meta:
        model = FeeStructure
        fields = [
            "id",
            "school",
            "classroom",
            "classroom_name",
            "amount",
            "term",
            "year"
        ]
        read_only_fields = ["school"]


class FeePaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    classroom_name = serializers.CharField(
        source="student.classroom.name",
        read_only=True
    )
    stream_name = serializers.CharField(
        source="student.stream.name",
        read_only=True
    )

    class Meta:
        model = FeePayment
        fields = [
            "id",
            "school",
            "student",
            "student_name",
            "classroom_name",
            "stream_name",
            "amount_paid",
            "payment_date",
            "term",
            "year",
            "created"
        ]
        read_only_fields = ["school"]

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class StudentFeeSummarySerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    classroom_name = serializers.CharField(
        source="classroom.name",
        read_only=True
    )
    stream_name = serializers.CharField(
        source="stream.name",
        read_only=True
    )
    total_fee = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "student_name",
            "admission_number",
            "classroom_name",
            "stream_name",
            "total_fee",
            "total_paid",
            "balance"
        ]

    def get_student_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_total_fee(self, obj):
        fee = FeeStructure.objects.filter(
            classroom=obj.classroom
        ).first()

        if fee:
            return fee.amount

        return 0

    def get_total_paid(self, obj):
        total = FeePayment.objects.filter(
            student=obj
        ).aggregate(
            total=Sum("amount_paid")
        )["total"]

        if total:
            return total

        return 0

    def get_balance(self, obj):
        fee = self.get_total_fee(obj)
        paid = self.get_total_paid(obj)

        return fee - paid


class ParentStudentFeeSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    classroom_name = serializers.CharField(
        source="classroom.name",
        read_only=True
    )
    stream_name = serializers.CharField(
        source="stream.name",
        read_only=True
    )
    total_fee = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "student_name",
            "admission_number",
            "classroom_name",
            "stream_name",
            "total_fee",
            "total_paid",
            "balance",
            "payments"
        ]

    def get_student_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_total_fee(self, obj):
        fee = FeeStructure.objects.filter(
            classroom=obj.classroom
        ).first()

        if fee:
            return fee.amount

        return 0

    def get_total_paid(self, obj):
        total = FeePayment.objects.filter(
            student=obj
        ).aggregate(
            total=Sum("amount_paid")
        )["total"]

        if total:
            return total

        return 0

    def get_balance(self, obj):
        fee = self.get_total_fee(obj)
        paid = self.get_total_paid(obj)

        return fee - paid

    def get_payments(self, obj):
        payments = FeePayment.objects.filter(
            student=obj
        ).order_by("-created")

        return FeePaymentSerializer(
            payments,
            many=True
        ).data

# class TimetableSerializer(serializers.ModelSerializer):

#     teacher_name = serializers.CharField(source="teacher.user.username", read_only=True)
#     subject_name = serializers.CharField(source="subject.name", read_only=True)
#     class_name = serializers.CharField(source="classroom.name", read_only=True)

#     class Meta:
#         model = Timetable
#         fields = "__all__"

#     def validate(self, data):
#         teacher = data.get("teacher")
#         subject = data.get("subject")

#         if subject not in teacher.subject.all():
#             raise serializers.ValidationError(
#                 "Teacher does not teach this subject"
#             )

#         return data

class TimetableSerializer(serializers.ModelSerializer):

    teacher_name = serializers.CharField(source="teacher.user.username", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    class_name = serializers.CharField(source="classroom.name", read_only=True)
    stream_name = serializers.CharField(source="stream.name", read_only=True)

    class Meta:
        model = Timetable
        fields = "__all__"

    def validate(self, data):

        teacher = data.get("teacher")
        subject = data.get("subject")
        day = data.get("day")
        start = data.get("start_time")
        end = data.get("end_time")

        # ✅ SUBJECT VALIDATION
        if subject not in teacher.subject.all():
            raise serializers.ValidationError(
                {"subject": "Teacher does not teach this subject"}
            )

        # ✅ TIME VALIDATION
        # if start >= end:
        #     raise serializers.ValidationError(
        #         {"time": "End time must be greater than start time"}
        #     )

        # ✅ CONFLICT DETECTION
        conflicts = Timetable.objects.filter(
            teacher=teacher,
            day=day,
            start_time__lt=end,
            end_time__gt=start
        )

        if conflicts.exists():
            raise serializers.ValidationError(
                {"conflict": "Teacher already has a class at this time"}
            )

        return data



class GradingSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradingSystem
        fields = "__all__"

############ inayotumika ni hii ya chini
class GradingSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradingSystem
        fields = "__all__"

class SchoolEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = "__all__"




class StudentBehaviourSerializer(serializers.ModelSerializer):

    student_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentBehaviour
        fields = '__all__'

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"



class ParentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentComment
        fields = "__all__"


class TeacherSchemeSerializer(serializers.ModelSerializer):

    teacher_name = serializers.CharField(source="teacher.user.username", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)
    stream_name = serializers.CharField(source="stream.name", read_only=True)

    class Meta:
        model = TeacherScheme
        fields = "__all__"







from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)

    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        if not CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No user found with this email"
            )

        return value


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):

        email = attrs.get("email")
        otp = attrs.get("otp")

        user = CustomerUser.objects.filter(
            email=email
        ).first()

        if not user:
            raise serializers.ValidationError(
                {"email": "User not found"}
            )

        otp_obj = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp,
            is_verified=False
        ).order_by("-created_at").first()

        if not otp_obj:
            raise serializers.ValidationError(
                {"otp": "Invalid OTP"}
            )

        if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
            raise serializers.ValidationError(
                {"otp": "OTP has expired"}
            )

        attrs["otp_obj"] = otp_obj
        attrs["user"] = user

        return attrs


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    new_password = serializers.CharField(
        validators=[validate_password]
    )

    confirm_password = serializers.CharField()

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )

        return attrs