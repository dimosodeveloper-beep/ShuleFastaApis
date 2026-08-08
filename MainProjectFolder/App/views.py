from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
#RegisterUser
from .models import *
from .serializers import *

#Latest
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *

#import numpy as np
#from scipy.optimize import linprog
from django.http import HttpResponse
from datetime import datetime, timedelta
#import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import os
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import requests

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
#UpdateDeleteGradingSystem
#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from App.serializers import *


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination

from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings
#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from App.serializers import *

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view
from django.db.models import Sum
from django.db import transaction
from django.utils.timezone import now, timedelta
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


import requests
from requests.auth import HTTPBasicAuth
import requests
from django.http import JsonResponse

from dotenv import load_dotenv
import os

import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import base64
import requests
# AddResult
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from .helpers import get_grade
#SendOTPView
# Load environment variables
load_dotenv()

class LatestVersionView(APIView):
    def get(self, request):
        latest_version = "7"
        return JsonResponse({"latest_version": latest_version})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Result, Student
from django.db.models import Avg, Sum, Count


import random

from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.utils import timezone
from datetime import timedelta




class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = request.user

            old_password = serializer.validated_data["old_password"]

            if not user.check_password(old_password):

                return Response(
                    {
                        "error": "Old password is incorrect"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(
                serializer.validated_data["new_password"]
            )

            user.save()

            return Response(
                {
                    "message": "Password changed successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class SendOTPView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        if serializer.is_valid():

            email = serializer.validated_data["email"]

            user = CustomerUser.objects.get(
                email=email
            )

            otp = str(
                random.randint(100000, 999999)
            )

            PasswordResetOTP.objects.create(
                user=user,
                otp=otp
            )

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is {otp}. It will expire in 5 minutes.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )

            return Response(
                {
                    "message": "OTP sent successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )






class VerifyOTPView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        if serializer.is_valid():

            otp_obj = serializer.validated_data[
                "otp_obj"
            ]

            otp_obj.is_verified = True

            otp_obj.save()

            return Response(
                {
                    "message": "OTP verified successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )





class ResetPasswordView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        if serializer.is_valid():

            email = serializer.validated_data["email"]

            user = CustomerUser.objects.get(
                email=email
            )

            otp_obj = PasswordResetOTP.objects.filter(
                user=user,
                is_verified=True
            ).order_by("-created_at").first()

            if not otp_obj:

                return Response(
                    {
                        "error": "OTP verification required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if timezone.now() > otp_obj.created_at + timedelta(minutes=5):

                return Response(
                    {
                        "error": "OTP expired"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(
                serializer.validated_data["new_password"]
            )

            user.save()

            otp_obj.delete()

            return Response(
                {
                    "message": "Password reset successful"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )





# def calculate_grade(avg):
#     if avg >= 80:
#         return "A"
#     elif avg >= 70:
#         return "B"
#     elif avg >= 50:
#         return "C"
#     elif avg >= 40:
#         return "D"
#     elif avg >= 30:
#         return "E"
#     else:
#         return "F"

def calculate_grade(avg, school):
    grading = GradingSystem.objects.filter(
        school=school,
        min_score__lte=avg,
        max_score__gte=avg
    ).first()

    if grading:
        return grading.grade

    return "N/A"

class DashboardStatsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        school = request.user.school

        # Count results for this school
        results_count = Result.objects.filter(school=school).count()

        # Count attendance entries
        attendance_count = Attendance.objects.filter(school=school).count()

        # Count exams
        exams_count = Exam.objects.filter(school=school).count()

        # Count students
        students_count = Student.objects.filter(school=school).count()

        data = {
            "results_count": results_count,
            "attendance_count": attendance_count,
            "exams_count": exams_count,
            "students_count": students_count,
        }

        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.db.models import Q
import re

User = get_user_model()
import re


User = get_user_model()

class RegisterUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        role = data.get('role')

        errors = {}

        # 🔥 REQUIRED FIELDS
        if not username: errors['username'] = ["Username is required"]
        if not email: errors['email'] = ["Email is required"]
        if not password: errors['password'] = ["Password is required"]
        if not confirm_password: errors['confirm_password'] = ["Confirm password is required"]

        # 🔥 VALIDATIONS
        if username and len(username) < 3:
            errors['username'] = ["Username must be at least 3 characters"]

        if email:
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_regex, email):
                errors['email'] = ["Invalid email address"]

        if password and len(password) < 8:
            errors['password'] = ["Password must be at least 8 characters"]

        common_passwords = ["123456", "password", "12345678", "qwerty", "111111"]
        if password and password.lower() in common_passwords:
            errors['password'] = ["Password is too common"]

        if password and confirm_password and password != confirm_password:
            errors['confirm_password'] = ["Passwords do not match"]

        if username and User.objects.filter(username=username).exists():
            errors['username'] = ["Username already exists"]

        if email and User.objects.filter(email=email).exists():
            errors['email'] = ["Email already exists"]

        if errors:
            return Response(errors, status=400)

        # 🔥 CREATE USER NA KUSET ADMIN PERMISSIONS
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            school=request.user.school
        )

        # HAPA NDIO LOGIC YA ADMIN IMESETIWA
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()

        token = Token.objects.create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }, status=201)



class LoginUser(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data['user']

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key
            })

        return Response(serializer.errors)



class CreateAcademicYear(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        data['school'] = request.user.school.id

        serializer = AcademicYearSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)



class GetAcademicYears(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        years = AcademicYear.objects.filter(
            school=request.user.school
        ).order_by("-year")

        serializer = AcademicYearSerializer(years, many=True)

        return Response(serializer.data)







class CreateSchool(APIView):

    def post(self, request):

        serializer = SchoolSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class CreateClassRoom(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        data['school'] = request.user.school.id

        serializer = ClassRoomSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class GetClasses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def get(self, request):

        classes = ClassRoom.objects.filter(
            school=request.user.school
        )

        serializer = ClassRoomSerializer(classes, many=True)

        return Response(serializer.data)



class CreateStream(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        data['school'] = request.user.school.id

        serializer = StreamSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)



class GetStreams(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def get(self, request, class_id):

        streams = Stream.objects.filter(
            classroom_id=class_id
        )

        serializer = StreamSerializer(streams, many=True)

        return Response(serializer.data)




# class CreateStudent(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     #permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data.copy()

#         data['school'] = request.user.school.id

#         serializer = StudentSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)

from datetime import datetime


class CreateStudent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        # 🔥 muhimu
        data['school'] = request.user.school.id

        classroom_id = data.get("classroom")
        stream_id = data.get("stream")

        # 🔥 remove zisije zikaharibu serializer
        data.pop("classroom", None)
        data.pop("stream", None)

        serializer = StudentSerializer(data=data)

        if serializer.is_valid():

            student = serializer.save()

            # 🔥 create enrollment automatically
            StudentEnrollment.objects.create(
                school=request.user.school,
                student=student,
                classroom_id=classroom_id,
                stream_id=stream_id,
                year=datetime.now().year
            )

            return Response({
                "student": StudentSerializer(student).data,
                "message": "Student created successfully with enrollment"
            })

        return Response(serializer.errors)


class GetParents(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        parents = CustomerUser.objects.filter(
            school=request.user.school,
            role="parent"
        )

        serializer = UserSerializer(parents, many=True)

        return Response(serializer.data)




# class GetTeachersSelectedField(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         teachers = CustomerUser.objects.filter(
#             school=request.user.school,
#             role="teacher"
#         )

#         serializer = UserSerializer(teachers, many=True)

#         return Response(serializer.data)


class GetTeachersSelectedField(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        teachers = Teacher.objects.filter(
            school=request.user.school
        )

        data = []

        for teacher in teachers:

            data.append({
                "id": teacher.id,
                "username": teacher.user.username,
                "phone": teacher.phone,
            })

        return Response(data)



class GetStudents(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def get(self, request):

        students = Student.objects.filter(
            school=request.user.school
        )

        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)




class GetStudents2_By_Class(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        classroom_id = request.GET.get("classroom")
        stream_id = request.GET.get("stream")
        year = request.GET.get("year")

        enrollments = StudentEnrollment.objects.filter(
            school=request.user.school
        )

        if classroom_id:
            enrollments = enrollments.filter(
                classroom_id=classroom_id
            )

        if stream_id:
            enrollments = enrollments.filter(
                stream_id=stream_id
            )

        if year:
            enrollments = enrollments.filter(
                year=year
            )

        students = Student.objects.filter(
            id__in=enrollments.values_list(
                "student_id",
                flat=True
            )
        ).distinct()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)


from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import StudentEnrollment


class GetStudentsInStream(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, stream_id):

        # ===============================
        # GET CURRENT YEAR FROM PYTHON
        # ===============================
        current_year = datetime.now().year

        enrollments = StudentEnrollment.objects.filter(
            school=request.user.school,
            classroom_id=class_id,
            stream_id=stream_id,
            year=current_year   # 🔥 FILTER BY CURRENT SYSTEM YEAR
        ).select_related("student", "classroom", "stream")

        students = []

        for enrollment in enrollments:

            st = enrollment.student

            students.append({
                "id": st.id,
                "first_name": st.first_name,
                "last_name": st.last_name,
                "admission_number": st.admission_number,
                "gender": st.gender,
                "classroom": enrollment.classroom.name,
                "stream": enrollment.stream.name,
                "year": enrollment.year
            })

        return Response(students)





# class GetStudentsInStream_for_students(APIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, class_id, stream_id, year):

#         # ===============================
#         # FIX: ENSURE YEAR IS INTEGER
#         # ===============================
#         current_year = int(year)

#         enrollments = StudentEnrollment.objects.filter(
#             school=request.user.school,
#             classroom_id=class_id,
#             stream_id=stream_id,
#             year=current_year
#         ).select_related(
#             "student",
#             "classroom",
#             "stream"
#         )

#         students = []

#         for enrollment in enrollments:

#             st = enrollment.student

#             students.append({
#                 "id": st.id,
#                 "first_name": st.first_name,
#                 "last_name": st.last_name,
#                 "admission_number": st.admission_number,
#                 "gender": st.gender,
#                 "classroom": enrollment.classroom.name,
#                 "stream": enrollment.stream.name,
#                 "year": enrollment.year
#             })

#         return Response(students)






class GetStudentsInStream_for_students(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, stream_id, year):

        # ===============================
        # DEBUG INPUT VALUES
        # ===============================
        current_year = int(year)

        debug_info = {
            "received_class_id": class_id,
            "received_stream_id": stream_id,
            "received_year": current_year,
            "user_school_id": request.user.school.id if request.user.school else None,
        }

        # ===============================
        # QUERY
        # ===============================
        enrollments = StudentEnrollment.objects.filter(
            school=request.user.school,
            classroom_id=class_id,
            stream_id=stream_id,
            year=current_year
        ).select_related(
            "student",
            "classroom",
            "stream"
        )

        # ===============================
        # RESULTS
        # ===============================
        students = []

        for enrollment in enrollments:

            st = enrollment.student

            students.append({
                "id": st.id,
                "first_name": st.first_name,
                "last_name": st.last_name,
                "admission_number": st.admission_number,
                "gender": st.gender,
                "classroom": enrollment.classroom.name,
                "stream": enrollment.stream.name,
                "year": enrollment.year
            })

        # ===============================
        # FINAL RESPONSE (WITH DEBUG)
        # ===============================
        return Response({
            "debug": debug_info,
            "count": len(students),
            "results": students
        })







####################################################################################
##kwa ajili ya kuadd subject

class GetClassrooms(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        school = request.user.school

        classrooms = ClassRoom.objects.filter(school=school)

        serializer = ClassRoomSubjectSerializer(classrooms, many=True)

        return Response(serializer.data)



class CreateSubject(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        data['school'] = request.user.school.id

        serializer = SubjectSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)



# class CreateSubject(APIView):

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data.copy()

#         data["school"] = request.user.school.id

#         serializer = SubjectSerializer(data=data)

#         if serializer.is_valid():

#             subject = serializer.save()

#             if "streams" in data:
#                 subject.streams.set(data["streams"])

#             if "classrooms" in data:
#                 subject.classrooms.set(data["classrooms"])

#             return Response(SubjectSerializer(subject).data)

#         return Response(serializer.errors)


class GetSubjects(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    permission_classes = [IsAuthenticated]

    def get(self, request):

        subjects = Subject.objects.filter(
            school=request.user.school
        )

        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import ExamCategory
from .serializers import ExamCategorySerializer


class CreateExamCategory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        # 👉 Auto assign school from logged-in user
        data['school'] = request.user.school.id

        serializer = ExamCategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class GetExamCategories(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 👉 Filter by user's school
        categories = ExamCategory.objects.filter(
            school=request.user.school
        )

        serializer = ExamCategorySerializer(categories, many=True)

        return Response(serializer.data)





class CreateExam(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        print("======== REQUEST DATA ========")
        print(request.data)

        print("======== USER ========")
        print(request.user)

        print("======== USER SCHOOL ========")
        print(request.user.school)

        if not request.user.school:
            return Response(
                {"error": "User hana school assigned"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CreateExamSerializer(
            data=request.data,
            context={'request': request}   # 🔥 MUHIMU SANA
        )

        if serializer.is_valid():
            exam = serializer.save()
            print("✅ EXAM CREATED:", exam)

            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        print("❌ SERIALIZER ERRORS:", serializer.errors)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class GetExams(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):

        exams = Exam.objects.filter(
            school=request.user.school
        )

        serializer = ExamSerializer(exams, many=True)

        return Response(serializer.data)



class GetExamsResults(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        category_id = request.GET.get("category_id")

        exams = Exam.objects.filter(
            school=request.user.school
        )

        # 👉 filter by category kama ipo
        if category_id:
            exams = exams.filter(category_id=category_id)

        serializer = ExamSerializer(exams, many=True)

        return Response(serializer.data)



from .helpers import get_grade



from datetime import datetime

from .helpers import get_grade


class AddResult(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        student_id = data.get("student")

        # 🔥 AUTO CURRENT YEAR
        current_year = datetime.now().year

        # 🔥 GET ENROLLMENT
        try:
            enrollment = StudentEnrollment.objects.get(
                student_id=student_id,
                year=current_year,
                school=request.user.school
            )
        except StudentEnrollment.DoesNotExist:
            return Response({
                "error": "Student hana enrollment ya mwaka huu"
            }, status=400)

        score = data.get("marks")

        grade = get_grade(int(score), request.user.school)

        # 🔥 SAVE RESULT (AUTO YEAR + SNAPSHOT)
        result = Result.objects.create(
            school=request.user.school,
            student_id=student_id,
            subject_id=data.get("subject"),
            exam_id=data.get("exam"),
            marks=score,
            grade=grade,
            classroom=enrollment.classroom,
            stream=enrollment.stream,
            year=current_year
        )

        return Response({
            "message": "Result saved successfully",
            "data": {
                "student": result.student.id,
                "marks": result.marks,
                "grade": result.grade,
                "year": result.year
            }
        })

from .helpers import get_grade


from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Result, StudentEnrollment
from .helpers import get_grade


class BulkResultUpload(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        results = request.data

        current_year = datetime.now().year  # 🔥 AUTO YEAR

        for item in results:

            student_id = item["student"]

            try:
                enrollment = StudentEnrollment.objects.get(
                    student_id=student_id,
                    year=current_year,
                    school=request.user.school
                )
            except StudentEnrollment.DoesNotExist:
                continue  # skip huyu mwanafunzi

            score = item["marks"]

            grade = get_grade(int(score), request.user.school)

            Result.objects.create(
                school=request.user.school,
                student_id=student_id,
                subject_id=item["subject"],
                exam_id=item["exam"],
                marks=score,
                grade=grade,
                classroom=enrollment.classroom,
                stream=enrollment.stream,
                year=current_year
            )

        return Response({
            "message": "Results saved successfully"
        })






from datetime import datetime
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Result, StudentEnrollment, Student
from .helpers import get_grade

import pandas as pd
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# class UploadResultsExcel(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         excel_file = request.FILES.get("file")

#         if not excel_file:
#             return Response({"error": "No excel file uploaded"}, status=400)

#         try:
#             df = pd.read_excel(excel_file)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)

#         current_year = datetime.now().year

#         saved_results = []
#         errors = []

#         for index, row in df.iterrows():

#             try:
#                 admission_number = str(row["admission_number"]).strip()
#                 subject_id = int(row["subject"])
#                 exam_id = int(row["exam"])
#                 marks = float(row["marks"])

#                 # student
#                 student = Student.objects.get(
#                     admission_number=admission_number,
#                     school=request.user.school
#                 )

#                 # enrollment (SAFE GET)
#                 enrollment = StudentEnrollment.objects.filter(
#                     student=student,
#                     school=request.user.school,
#                     year=current_year
#                 ).order_by("-id").first()

#                 if not enrollment:
#                     raise Exception("Student enrollment not found for current year")

#                 # exam & subject validation
#                 exam = Exam.objects.get(id=exam_id, school=request.user.school)
#                 subject = Subject.objects.get(id=subject_id, school=request.user.school)

#                 grade = get_grade(int(marks), request.user.school)

#                 result = Result.objects.create(
#                     school=request.user.school,
#                     student=student,
#                     classroom=enrollment.classroom,
#                     stream=enrollment.stream,
#                     year=current_year,
#                     exam=exam,
#                     subject=subject,
#                     marks=marks,
#                     grade=grade
#                 )

#                 saved_results.append({
#                     "student": student.first_name,
#                     "marks": marks,
#                     "grade": grade
#                 })

#             except Exception as e:
#                 errors.append({
#                     "row": index + 1,
#                     "error": str(e)
#                 })

#         return Response({
#             "message": "Excel uploaded successfully",
#             "saved_results": saved_results,
#             "errors": errors
#         })





class UploadResultsExcel(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        excel_file = request.FILES.get("file")

        if not excel_file:
            return Response({"error": "No excel file uploaded"}, status=400)

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({"error": f"Invalid Excel file: {str(e)}"}, status=400)

        current_year = datetime.now().year

        saved_results = []
        errors = []

        for index, row in df.iterrows():

            try:
                admission_number = str(row["admission_number"]).strip()
                subject_id = int(row["subject"])
                exam_id = int(row["exam"])
                marks = float(row["marks"])

                student = Student.objects.get(
                    admission_number=admission_number,
                    school=request.user.school
                )

                enrollment = StudentEnrollment.objects.filter(
                    student=student,
                    school=request.user.school,
                    year=current_year
                ).order_by("-id").first()

                if not enrollment:
                    raise Exception("Student not enrolled in current year")

                exam = Exam.objects.get(id=exam_id, school=request.user.school)
                subject = Subject.objects.get(id=subject_id, school=request.user.school)

                grade = get_grade(int(marks), request.user.school)

                result = Result.objects.create(
                    school=request.user.school,
                    student=student,
                    classroom=enrollment.classroom,
                    stream=enrollment.stream,
                    year=current_year,
                    exam=exam,
                    subject=subject,
                    marks=marks,
                    grade=grade
                )

                saved_results.append({
                    "student": student.first_name,
                    "marks": marks,
                    "grade": grade
                })

            except Exception as e:
                errors.append({
                    "row": index + 1,
                    "error": str(e)
                })

        # =========================
        # 🔥 SMART RESPONSE LOGIC
        # =========================

        if len(saved_results) == 0:

            return Response({
                "status": "failed",
                "message": "No results were uploaded. Please check Excel format and data.",
                "errors": errors
            }, status=400)

        if len(errors) > 0:

            return Response({
                "status": "partial_success",
                "message": "Some results uploaded but others failed.",
                "saved_count": len(saved_results),
                "error_count": len(errors),
                "saved_results": saved_results,
                "errors": errors
            }, status=207)

        return Response({
            "status": "success",
            "message": "All results uploaded successfully",
            "saved_count": len(saved_results),
            "saved_results": saved_results
        }, status=200)







class GetExamResults(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):

        results = Result.objects.filter(
            exam_id=exam_id,
            school=request.user.school
        )

        serializer = ResultSerializer(results, many=True)

        return Response(serializer.data)







################# RESULTS NEW STARTING HERE ########################
class GetExamClasses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):

        exam = Exam.objects.get(id=exam_id, school=request.user.school)

        classes = exam.classrooms.all()

        data = [
            {
                "id": c.id,
                "name": c.name
            }
            for c in classes
        ]

        return Response(data)


from django.db.models import Avg, Count


from django.db.models import Sum

class GetStudentsResults(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        class_id = request.GET.get("class_id")
        exam_id = request.GET.get("exam_id")
        year = request.GET.get("year")

        results = Result.objects.filter(
            school=request.user.school,
            classroom_id=class_id,
            exam_id=exam_id,
            year=year
        )

        students_ids = results.values_list("student_id", flat=True).distinct()

        students = Student.objects.filter(
            id__in=students_ids,
            school=request.user.school
        )

        data = []

        for student in students:
            student_results = results.filter(student=student)

            total_marks = student_results.aggregate(total=Sum("marks"))["total"] or 0
            exams_count = student_results.count()

            avg = total_marks / exams_count if exams_count > 0 else 0

            grade = calculate_grade(avg, request.user.school)

            data.append({
                "student_id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "total_marks": total_marks,
                "exams_count": exams_count,
                "average": round(avg, 2),
                "grade": grade
            })

        data = sorted(data, key=lambda x: x["average"], reverse=True)

        return Response(data)





class GetSingleStudentResults(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):

        exam_id = request.GET.get('exam_id')
        year = request.GET.get('year')

        results = Result.objects.filter(
            student_id=student_id,
            exam_id=exam_id,
            year=year,
            school=request.user.school
        )

        if not results.exists():
            return Response({
                "student_id": student_id,
                "total_marks": 0,
                "average": 0,
                "grade": "F",
                "details": []
            })

        total_marks = results.aggregate(total=Sum("marks"))["total"] or 0
        subjects_count = results.count()

        avg = total_marks / subjects_count if subjects_count > 0 else 0

        grade = calculate_grade(avg, request.user.school)

        data = {
            "student_id": student_id,
            "total_marks": total_marks,
            "average": round(avg, 2),
            "grade": grade,
            "details": [
                {
                    "subject": r.subject.name,
                    "marks": r.marks,
                    "exam": r.exam.name,
                    "exam_date": r.exam.date,
                    "year": r.year,
                    "class": r.classroom.name,
                    "grade": calculate_grade(r.marks, request.user.school)
                }
                for r in results
            ]
        }

        return Response(data)

class ResultsSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        class_id = request.GET.get("class_id")
        exam_id = request.GET.get("exam_id")
        year = request.GET.get("year")

        results = Result.objects.filter(
            school=request.user.school,
            classroom_id=class_id,
            exam_id=exam_id,
            year=year
        )

        students_ids = results.values_list("student_id", flat=True).distinct()

        students = Student.objects.filter(
            id__in=students_ids,
            school=request.user.school
        )

        summary_list = []

        grades = GradingSystem.objects.filter(school=request.user.school)
        grade_count = {g.grade: 0 for g in grades}

        for student in students:
            student_results = results.filter(student=student)

            total = student_results.aggregate(total=Sum("marks"))["total"] or 0
            count = student_results.count()

            avg = total / count if count > 0 else 0

            grade = calculate_grade(avg, request.user.school)

            if grade in grade_count:
                grade_count[grade] += 1

            summary_list.append({
                "name": f"{student.first_name} {student.last_name}",
                "average": round(avg, 2)
            })

        summary_list = sorted(summary_list, key=lambda x: x["average"], reverse=True)

        return Response({
            "top_10": summary_list[:10],
            "last_10": sorted(summary_list[-10:], key=lambda x: x["average"]),
            "grades": grade_count
        })

#################RANKING ####################################

class StudentReportCard(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, exam_id):

        student = Student.objects.get(id=student_id)

        results = Result.objects.filter(
            student_id=student_id,
            exam_id=exam_id,
            school=request.user.school
        )

        subjects = []
        total = 0
        count = 0

        for r in results:

            subjects.append({
                "subject": r.subject.name,
                "marks": r.marks
            })

            total += r.marks
            count += 1

        average = total / count if count > 0 else 0

        return Response({
            "student": f"{student.first_name} {student.last_name}",
            "subjects": subjects,
            "total_marks": total,
            "average": average
        })


class ClassRanking(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, exam_id):

        students = Student.objects.filter(
            classroom_id=class_id,
            school=request.user.school
        )

        data = []

        for student in students:

            results = Result.objects.filter(
                student=student,
                exam_id=exam_id
            )

            total = 0
            count = 0

            for r in results:
                total += r.marks
                count += 1

            average = total / count if count > 0 else 0

            data.append({
                "student_id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "average": average
            })

        sorted_data = sorted(
            data,
            key=lambda x: x["average"],
            reverse=True
        )

        position = 1

        for item in sorted_data:
            item["position"] = position
            position += 1

        return Response(sorted_data)



class StreamRanking(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, stream_id, exam_id):

        students = Student.objects.filter(
            stream_id=stream_id,
            school=request.user.school
        )

        data = []

        for student in students:

            results = Result.objects.filter(
                student=student,
                exam_id=exam_id
            )

            total = 0
            count = 0

            for r in results:
                total += r.marks
                count += 1

            average = total / count if count > 0 else 0

            data.append({
                "student_id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "average": average
            })

        sorted_data = sorted(
            data,
            key=lambda x: x["average"],
            reverse=True
        )

        position = 1

        for item in sorted_data:
            item["position"] = position
            position += 1

        return Response(sorted_data)



############ TO 10 Students ################

class TopStudents(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, exam_id):

        students = Student.objects.filter(
            classroom_id=class_id,
            school=request.user.school
        )

        data = []

        for student in students:

            results = Result.objects.filter(
                student=student,
                exam_id=exam_id
            )

            total = 0
            count = 0

            for r in results:
                total += r.marks
                count += 1

            average = total / count if count > 0 else 0

            data.append({
                "student": f"{student.first_name} {student.last_name}",
                "average": average
            })

        sorted_data = sorted(
            data,
            key=lambda x: x["average"],
            reverse=True
        )

        top10 = sorted_data[:10]

        position = 1

        for item in top10:
            item["position"] = position
            position += 1

        return Response(top10)









############## ATTENDANCE ##################################

class TakeAttendance(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        data['school'] = request.user.school.id

        serializer = CreateAttendanceSerializer(data=data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "message": "Attendance saved",
                "data": serializer.data
            })

        return Response(serializer.errors)


# Bulk Attendance (VERY IMPORTANT)

# Walimu wengi watachukua attendance ya darasa zima kwa wakati mmoja.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from datetime import date


# class BulkAttendance(APIView):
#     authentication_classes = [TokenAuthentication]

#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data

#         if not isinstance(data, list):
#             return Response({"error": "Expected a list of attendance records"}, status=400)

#         for item in data:

#             if not all(k in item for k in ["student", "classroom", "stream", "status"]):
#                 return Response({"error": "Missing fields in one of the records"}, status=400)

#             Attendance.objects.update_or_create(
#                 student_id=item["student"],
#                 date=item.get("date", date.today()),
#                 defaults={
#                     "school": request.user.school,
#                     "classroom_id": item["classroom"],
#                     "stream_id": item["stream"],
#                     "status": item["status"]
#                 }
#             )

#         return Response({
#             "message": "Attendance recorded successfully"
#         })
from datetime import date


class BulkAttendance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data

        if not isinstance(data, list):
            return Response(
                {"error": "Expected a list of attendance records"},
                status=400
            )

        created_records = []

        current_year = date.today().year

        for item in data:

            if not all(
                k in item
                for k in ["student", "classroom", "stream", "status"]
            ):
                return Response(
                    {"error": "Missing fields in one of the records"},
                    status=400
                )

            attendance = Attendance.objects.create(
                school=request.user.school,
                student_id=item["student"],
                classroom_id=item["classroom"],
                stream_id=item["stream"],
                year=current_year,
                status=item["status"],
                reason=item.get("reason", ""),
                date=item.get("date", date.today())
            )

            created_records.append(attendance.id)

        return Response({
            "message": "Attendance recorded successfully",
            "records_created": created_records
        })



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Attendance

from datetime import date

from collections import defaultdict
from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import Sum






class GetAttendanceByDate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, stream_id):

        selected_date = request.GET.get("date")
        status = request.GET.get("status")

        if not selected_date:
            selected_date = date.today()

        attendance = Attendance.objects.filter(
            classroom_id=class_id,
            stream_id=stream_id,
            date=selected_date,
            school=request.user.school
        ).select_related("student").order_by("-created")

        if status:
            attendance = attendance.filter(status=status)

        grouped_data = {}

        for item in attendance:

            session_key = item.created.strftime("%H:%M")

            if session_key not in grouped_data:
                grouped_data[session_key] = []

            grouped_data[session_key].append({
                "id": item.id,
                "student_id": item.student.id,
                "name": f"{item.student.first_name} {item.student.last_name}",
                "admission_number": item.student.admission_number,
                "status": item.status,
                "reason": item.reason,
                "created": item.created.strftime("%H:%M:%S")
            })

        final_data = []

        for session in sorted(grouped_data.keys(), reverse=True):

            final_data.append({
                "session_time": session,
                "students": grouped_data[session]
            })

        return Response(final_data)








class StreamStudentsAttendanceStats(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, stream_id):

        enrollments = StudentEnrollment.objects.filter(
            classroom_id=class_id,
            stream_id=stream_id,
            school=request.user.school
        ).select_related("student")

        data = []

        for enrollment in enrollments:

            st = enrollment.student

            present = Attendance.objects.filter(
                student=st,
                classroom_id=class_id,
                stream_id=stream_id,
                school=request.user.school,
                status="present"
            ).count()

            absent = Attendance.objects.filter(
                student=st,
                classroom_id=class_id,
                stream_id=stream_id,
                school=request.user.school,
                status="absent"
            ).count()

            total = present + absent

            percentage = 0

            if total > 0:
                percentage = round((present / total) * 100, 1)

            data.append({
                "id": st.id,
                "name": f"{st.first_name} {st.last_name}",
                "admission_number": st.admission_number,
                "present": present,
                "absent": absent,
                "percentage": percentage,
                "classroom": enrollment.classroom.name,
                "stream": enrollment.stream.name,
                "year": enrollment.year
            })

        return Response(data)








class AttendanceStatistics(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):

        try:

            student = Student.objects.get(
                id=student_id,
                school=request.user.school
            )

        except Student.DoesNotExist:

            return Response({
                "student": None,
                "present_days": 0,
                "absent_days": 0,
                "timeline": []
            })

        attendance = Attendance.objects.filter(
            student=student,
            school=request.user.school
        ).order_by("-date", "-created")

        present = attendance.filter(status="present").count()

        absent = attendance.filter(status="absent").count()

        latest_enrollment = StudentEnrollment.objects.filter(
            student=student,
            school=request.user.school
        ).order_by("-created").first()

        classroom_name = None
        stream_name = None

        if latest_enrollment:
            classroom_name = latest_enrollment.classroom.name
            stream_name = latest_enrollment.stream.name

        timeline = []

        for att in attendance:

            timeline.append({
                "date": att.date.strftime("%Y-%m-%d"),
                "status": att.status
            })

        return Response({
            "student": {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "admission_number": student.admission_number,
                "gender": student.gender,
                "classroom": classroom_name,
                "stream": stream_name
            },
            "present_days": present,
            "absent_days": absent,
            "timeline": timeline
        })









class StudentAttendanceHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):

        attendance = Attendance.objects.filter(
            student_id=student_id,
            school=request.user.school
        ).order_by("-date")

        serializer = CreateAttendanceSerializer(
            attendance,
            many=True
        )

        return Response(serializer.data)


# views.py (ADD PROMOTION SYSTEM – FULL CODE)
# Promote Single Student

class PromoteStudent(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = StudentPromotionSerializer(data=request.data)

        if serializer.is_valid():

            student_id = serializer.validated_data["student"]
            classroom_id = serializer.validated_data["new_classroom"]
            stream_id = serializer.validated_data["new_stream"]

            student = Student.objects.get(id=student_id)

            student.classroom_id = classroom_id
            student.stream_id = stream_id

            student.save()

            return Response({
                "message": "Student promoted successfully"
            })

        return Response(serializer.errors)


# Promote Whole Class

class PromoteClass(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        class_id = request.data.get("classroom")
        new_class = request.data.get("new_classroom")

        students = Student.objects.filter(
            classroom_id=class_id,
            school=request.user.school
        )

        for student in students:

            student.classroom_id = new_class
            student.save()

        return Response({
            "message": "Class promoted successfully"
        })






# Parent Portal APIs
# Get Children of Parent

class ParentChildren(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):

        children = Student.objects.filter(
            parent=request.user
        )

        serializer = StudentSerializer(children, many=True)

        return Response(serializer.data)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import Sum

from .models import Result, Student




# ==================== API VIEW ====================
# class ParentChildResults(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, student_id, exam_id):

#         # 1️⃣ Hakikisha student ni wa parent
#         try:
#             student = Student.objects.get(
#                 id=student_id,
#                 parent=request.user,
#                 school=request.user.school
#             )
#         except Student.DoesNotExist:
#             return Response({
#                 "error": "Student not found or not yours"
#             }, status=404)

#         # 2️⃣ STRICT FILTER (HAPA NDIPO FIX KUBWA IPO)
#         results = Result.objects.select_related(
#             "subject",
#             "exam"
#         ).filter(
#             student=student,
#             exam__id=exam_id,          # 🔥 muhimu sana
#             exam__school=request.user.school,
#             school=request.user.school
#         )

#         # DEBUG (optional)
#         print("EXAM ID => ", exam_id)
#         print("RESULT COUNT => ", results.count())

#         if not results.exists():
#             return Response({
#                 "message": "No results found for this exam"
#             }, status=404)

#         # 3️⃣ CALCULATIONS
#         total_marks = results.aggregate(total=Sum("marks"))["total"] or 0
#         subjects_count = results.count()
#         avg = total_marks / subjects_count if subjects_count > 0 else 0
#         avg_grade = calculate_grade(avg, request.user.school)  # 🔥 full fix

#         # 4️⃣ CLEAN DETAILS (ADD GRADE PER SUBJECT)
#         details = []
#         for r in results:
#             details.append({
#                 "subject": r.subject.name,
#                 "marks": float(r.marks),
#                 "exam": r.exam.name,
#                 "exam_date": r.exam.date,
#                 "grade": calculate_grade(r.marks, request.user.school)  # 🔥 per subject grade
#             })

#         # 5️⃣ RESPONSE DATA
#         data = {
#             "student_id": student.id,
#             "name": f"{student.first_name} {student.last_name}",
#             "total_marks": float(total_marks),
#             "exams_count": 1,
#             "average": round(avg, 2),
#             "grade": avg_grade,  # 🔥 overall grade
#             "details": details
#         }

#         return Response(data)



# class ParentChildResults(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, student_id, exam_id):

#         year = request.GET.get("year")

#         # 🔥 ensure child belongs to parent
#         try:
#             student = Student.objects.get(
#                 id=student_id,
#                 parent=request.user,
#                 school=request.user.school
#             )
#         except Student.DoesNotExist:
#             return Response({"error": "Student not found"}, status=404)

#         results = Result.objects.filter(
#             student=student,
#             exam_id=exam_id,
#             year=year,
#             school=request.user.school
#         ).select_related("subject", "exam")

#         if not results.exists():
#             return Response({"message": "No results found"}, status=404)

#         total = results.aggregate(total=Sum("marks"))["total"] or 0
#         count = results.count()

#         avg = total / count

#         grade = calculate_grade(avg, request.user.school)

#         return Response({
#             "student_id": student.id,
#             "name": f"{student.first_name} {student.last_name}",
#             "total_marks": total,
#             "average": round(avg, 2),
#             "grade": grade,
#             "details": [
#                 {
#                     "subject": r.subject.name,
#                     "marks": r.marks,
#                     "exam": r.exam.name,
#                     "year": r.year,
#                     "grade": calculate_grade(r.marks, request.user.school)
#                 }
#                 for r in results
#             ]
#         })





class ParentChildResults(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, exam_id):

        year = request.GET.get("year")

        # =========================
        # 1. VERIFY CHILD BELONGS TO PARENT
        # =========================
        try:
            student = Student.objects.get(
                id=student_id,
                parent=request.user,   # OK FIXED
                school=request.user.school
            )
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        # =========================
        # 2. STUDENT RESULTS
        # =========================
        results = Result.objects.filter(
            student=student,
            exam_id=exam_id,
            year=year,
            school=request.user.school
        ).select_related("subject", "exam")

        if not results.exists():
            return Response({"message": "No results found"}, status=404)

        total = results.aggregate(total=Sum("marks"))["total"] or 0
        avg = total / results.count()

        # =========================
        # 3. CLASS RANKING
        # =========================
        class_students = Student.objects.filter(
            school=request.user.school,
            enrollments__classroom=student.enrollments.last().classroom,
            enrollments__year=year
        ).distinct()

        class_ranks = []

        for s in class_students:
            s_total = Result.objects.filter(
                student=s,
                exam_id=exam_id,
                year=year,
                school=request.user.school
            ).aggregate(total=Sum("marks"))["total"] or 0

            class_ranks.append({
                "student_id": s.id,
                "name": f"{s.first_name} {s.last_name}",
                "total": s_total
            })

        class_ranks = sorted(class_ranks, key=lambda x: x["total"], reverse=True)

        class_position = next(
            (i+1 for i, x in enumerate(class_ranks) if x["student_id"] == student.id),
            None
        )

        # =========================
        # 4. STREAM RANKING
        # =========================
        stream_students = Student.objects.filter(
            school=request.user.school,
            enrollments__stream=student.enrollments.last().stream,
            enrollments__year=year
        ).distinct()

        stream_ranks = []

        for s in stream_students:
            s_total = Result.objects.filter(
                student=s,
                exam_id=exam_id,
                year=year,
                school=request.user.school
            ).aggregate(total=Sum("marks"))["total"] or 0

            stream_ranks.append({
                "student_id": s.id,
                "name": f"{s.first_name} {s.last_name}",
                "total": s_total
            })

        stream_ranks = sorted(stream_ranks, key=lambda x: x["total"], reverse=True)

        stream_position = next(
            (i+1 for i, x in enumerate(stream_ranks) if x["student_id"] == student.id),
            None
        )

        # =========================
        # 5. GRAPH DATA (CLASS + STREAM)
        # =========================
        class_graph = [
            {"name": x["name"], "value": x["total"]}
            for x in class_ranks
        ]

        stream_graph = [
            {"name": x["name"], "value": x["total"]}
            for x in stream_ranks
        ]

        # =========================
        # RESPONSE
        # =========================
        return Response({
            "student_id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "total_marks": total,
            "average": round(avg, 2),
            "grade": avg,

            # 🔥 NEW FEATURES
            "class_position": class_position,
            "stream_position": stream_position,

            "class_total_students": len(class_ranks),
            "stream_total_students": len(stream_ranks),

            # 🔥 GRAPH DATA
            "class_graph": class_graph,
            "stream_graph": stream_graph,

            "details": [
                {
                    "subject": r.subject.name,
                    "marks": r.marks,
                    "exam": r.exam.name,
                    "year": r.year,
                    "grade": r.grade
                }
                for r in results
            ]
        })





# Report Card Data API (For PDF)

# API hii inatoa data kamili ya report card.

class ReportCardData(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, exam_id):

        student = Student.objects.get(id=student_id)

        results = Result.objects.filter(
            student_id=student_id,
            exam_id=exam_id
        )

        subjects = []
        total = 0
        count = 0

        for r in results:

            subjects.append({
                "subject": r.subject.name,
                "marks": r.marks
            })

            total += r.marks
            count += 1

        average = total / count if count > 0 else 0

        return Response({

            "student_name": f"{student.first_name} {student.last_name}",

            "classroom": student.classroom.name,

            "stream": student.stream.name,

            "subjects": subjects,

            "total": total,

            "average": average

        })








# # Fee Structure APIs
# # Create Fee Structure

# class CreateFeeStructure(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data.copy()

#         data['school'] = request.user.school.id

#         serializer = FeeStructureSerializer(data=data)

#         if serializer.is_valid():

#             serializer.save()

#             return Response(serializer.data)

#         return Response(serializer.errors)


# # Get Fee Structure

# class GetFeeStructure(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         fees = FeeStructure.objects.filter(
#             school=request.user.school
#         )

#         serializer = FeeStructureSerializer(fees, many=True)

#         return Response(serializer.data)


# # Fee Payment APIs
# # Pay Fee

# class PayFee(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data.copy()

#         data['school'] = request.user.school.id

#         serializer = FeePaymentSerializer(data=data)

#         if serializer.is_valid():

#             serializer.save()

#             return Response(serializer.data)

#         return Response(serializer.errors)


# ####  Student Fee History

# class StudentFeeHistory(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request, student_id):

#         payments = FeePayment.objects.filter(
#             student_id=student_id,
#             school=request.user.school
#         )

#         serializer = FeePaymentSerializer(payments, many=True)

#         return Response(serializer.data)








class CreateFeeStructure(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = FeeStructureSerializer(data=request.data)

        if serializer.is_valid():

            # 🔥 FORCE SAVE SCHOOL HERE (NOT IN DATA)
            serializer.save(school=request.user.school)

            return Response(serializer.data)

        return Response(serializer.errors)



# ======================================================
# GET ALL FEE STRUCTURES
# ======================================================

class GetFeeStructures(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        fees = FeeStructure.objects.filter(
            school=request.user.school
        ).order_by("-id")

        serializer = FeeStructureSerializer(
            fees,
            many=True
        )

        return Response(serializer.data)


# ======================================================
# CREATE FEE PAYMENT
# ======================================================

class CreateFeePayment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = FeePaymentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(school=request.user.school)
            return Response(serializer.data)

        return Response(serializer.errors)


# ======================================================
# GET ALL FEE PAYMENTS
# ======================================================

class GetFeePayments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = FeePayment.objects.filter(
            school=request.user.school
        ).order_by("-created")

        serializer = FeePaymentSerializer(
            payments,
            many=True
        )

        return Response(serializer.data)


# ======================================================
# GET SINGLE STUDENT FEE SUMMARY
# ======================================================

class GetStudentFeeSummary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):

        try:
            student = Student.objects.get(
                id=student_id,
                school=request.user.school
            )

        except Student.DoesNotExist:
            return Response({
                "error": "Student not found"
            })

        serializer = StudentFeeSummarySerializer(student)

        return Response(serializer.data)


# ======================================================
# GET ALL STUDENTS FEES SUMMARY
# ======================================================

class GetAllStudentsFeeSummary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        students = Student.objects.filter(
            school=request.user.school
        ).order_by("-id")

        serializer = StudentFeeSummarySerializer(
            students,
            many=True
        )

        return Response(serializer.data)


# ======================================================
# PARENT VIEW OWN CHILD FEES ONLY
# ======================================================

class ParentStudentFeesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            student = Student.objects.get(
                parent=request.user
            )

        except Student.DoesNotExist:
            return Response({
                "error": "No child found for this parent"
            })

        serializer = ParentStudentFeeSerializer(student)

        return Response(serializer.data)










##################### PART 02###########################################

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import FeeStructure, FeePayment, Student
from .serializers import FeePaymentSerializer


# ======================================================
# 1. GET AVAILABLE YEARS (FROM FEE STRUCTURE)
# ======================================================
class GetFeeYears(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        years = FeeStructure.objects.filter(
            school=request.user.school
        ).values_list("year", flat=True).distinct().order_by("-year")

        return Response(years)


# ======================================================
# 2. GET STUDENTS BY SCHOOL (FILTERED FOR PARENT/ADMIN)
# ======================================================


class GetStudentsByYear(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, year):

        enrollments = StudentEnrollment.objects.filter(
            school=request.user.school,
            year=year
        ).select_related(
            "student",
            "classroom",
            "stream"
        )

        # ======================================
        # PARENT RESTRICTION
        # ======================================

        if request.user.role == "parent":

            enrollments = enrollments.filter(
                student__parent=request.user
            )

        data = []

        for enrollment in enrollments:

            s = enrollment.student

            data.append({

                "id": s.id,

                "name": f"{s.first_name} {s.last_name}",

                "classroom": enrollment.classroom.name,

                "stream": enrollment.stream.name

            })

        return Response(data)

# ======================================================
# 3. GET STUDENT PAYMENTS GROUPED BY TERM (YEAR FILTER)
# ======================================================
class GetStudentYearPayments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, year):

        payments = FeePayment.objects.filter(
            school=request.user.school,
            student_id=student_id,
            year=year
        ).order_by("term", "-payment_date")

        grouped = {}

        for p in payments:
            if p.term not in grouped:
                grouped[p.term] = {
                    "term": p.term,
                    "total_paid": 0,
                    "payments": []
                }

            grouped[p.term]["payments"].append(FeePaymentSerializer(p).data)
            grouped[p.term]["total_paid"] += p.amount_paid

        return Response(grouped)

































# Dashboard Analytics APIs

# API hizi zinaonyesha statistics za shule.

# School Dashboard

class SchoolDashboard(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_students = Student.objects.filter(
            school=request.user.school
        ).count()

        total_teachers = Teacher.objects.filter(
            school=request.user.school
        ).count()

        total_classes = ClassRoom.objects.filter(
            school=request.user.school
        ).count()

        total_subjects = Subject.objects.filter(
            school=request.user.school
        ).count()

        return Response({

            "total_students": total_students,

            "total_teachers": total_teachers,

            "total_classes": total_classes,

            "total_subjects": total_subjects

        })


# Fee Dashboard

class FeeDashboard(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_payments = FeePayment.objects.filter(
            school=request.user.school
        )

        total_amount = sum(
            payment.amount_paid for payment in total_payments
        )

        return Response({

            "total_collected": total_amount,

            "total_transactions": total_payments.count()

        })







# # CREATE TIMETABLE
# class CreateTimetable(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data.copy()
#         data['school'] = request.user.school.id

#         serializer = TimetableSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)

class CreateTimetable(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()
        data['school'] = request.user.school.id

        serializer = TimetableSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

# GET CLASS TIMETABLE
class ClassTimetable(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):

        timetable = Timetable.objects.filter(
            classroom_id=class_id,
            school=request.user.school
        ).order_by("day","start_time")

        serializer = TimetableSerializer(timetable, many=True)

        return Response(serializer.data)


# GET CLASSES
class GetClasses2(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        classes = ClassRoom.objects.filter(
            school=request.user.school
        )

        data = [
            {"id": c.id, "name": c.name}
            for c in classes
        ]

        return Response(data)


# GET TEACHERS
class GetTeachers2(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        teachers = Teacher.objects.filter(
            school=request.user.school
        )

        data = [
            {
                "id": t.id,
                "name": t.user.username
            }
            for t in teachers
        ]

        return Response(data)



class GetSubjects2(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        subjects = Subject.objects.filter(
            school=request.user.school
        )

        data = [
            {"id": s.id, "name": s.name}
            for s in subjects
        ]

        return Response(data)


###########################################

class GenerateReportCard(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):

        student = Student.objects.get(id=student_id)

        results = Result.objects.filter(student=student)

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        p = canvas.Canvas(response)

        p.drawString(100, 800, "Student Report Card")

        p.drawString(100, 770, f"Student: {student.user.username}")

        y = 730

        for result in results:

            grade = get_grade(result.score, request.user.school)

            text = f"{result.subject.name} : {result.score} ({grade})"

            p.drawString(100, y, text)

            y -= 30

        p.showPage()

        p.save()

        return response




############  TEACHERS #################


class GetTeacherUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = CustomerUser.objects.filter(
            school=request.user.school,
            role="teacher"
        )

        data = [
            {
                "id": user.id,
                "username": user.username
            }
            for user in users
        ]

        return Response(data)


class CreateTeacher(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        subjects = data.get("subject", [])

        data['school'] = request.user.school.id

        serializer = TeacherSerializer(data=data)

        if serializer.is_valid():
            teacher = serializer.save()

            if subjects:
                teacher.subject.set(subjects)

            return Response(serializer.data)

        return Response(serializer.errors)


class GetTeachers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        teachers = Teacher.objects.filter(
            school=request.user.school
        )

        serializer = TeacherSerializer(teachers, many=True)

        return Response(serializer.data)


class GetSingleTeacher(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        teacher = Teacher.objects.get(id=id, school=request.user.school)

        serializer = TeacherSerializer(teacher)

        return Response(serializer.data)







############## CALENDER ##########################



class CreateEventView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        data['school'] = request.user.school.id

        serializer = SchoolEventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class GetEventsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = SchoolEvent.objects.filter(school=request.user.school)
        serializer = SchoolEventSerializer(events, many=True)
        return Response(serializer.data)





############## ########### GRADING ##################################################

class CreateGradingSystem(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        # 👉 Auto assign school from logged-in user
        data['school'] = request.user.school.id

        serializer = GradingSystemSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


class GetGradingSystem(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = GradingSystem.objects.filter(school=request.user.school)
        serializer = GradingSystemSerializer(data, many=True)
        return Response(serializer.data)


class UpdateDeleteGradingSystem(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        grading = GradingSystem.objects.get(id=pk, school=request.user.school)

        serializer = GradingSystemSerializer(grading, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        grading = GradingSystem.objects.get(id=pk, school=request.user.school)
        grading.delete()
        return Response({"message": "Deleted"})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Sum

from django.db.models import Sum

class GetAllReportCards(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        class_id = request.GET.get("class_id")

        exam_id = request.GET.get("exam_id")

        year = request.GET.get("year")

        results = Result.objects.filter(
            school=request.user.school,
            classroom_id=class_id,
            exam_id=exam_id,
            year=year
        ).select_related(
            "student",
            "classroom",
            "stream"
        )

        student_ids = results.values_list(
            "student_id",
            flat=True
        ).distinct()

        students = Student.objects.filter(
            id__in=student_ids,
            school=request.user.school
        )

        data = []

        grade_count = {}

        for student in students:

            student_results = results.filter(
                student=student
            )

            if not student_results.exists():
                continue

            total_marks = student_results.aggregate(
                total=Sum("marks")
            )["total"] or 0

            exams_count = student_results.count()

            avg = total_marks / exams_count if exams_count > 0 else 0

            grade = calculate_grade(
                avg,
                request.user.school
            )

            grade_count[grade] = grade_count.get(
                grade,
                0
            ) + 1

            first_result = student_results.first()

            data.append({

                "student_id": student.id,

                "name": f"{student.first_name} {student.last_name}",

                "class": first_result.classroom.name,

                "stream": first_result.stream.name,

                "total_marks": total_marks,

                "exams_count": exams_count,

                "average": round(avg,2),

                "grade": grade,

                "parent_email": student.parent.email if student.parent else None,

                "parent_name": f"{student.parent.first_name} {student.parent.last_name}" if student.parent else None

            })

        data = sorted(
            data,
            key=lambda x:x["average"],
            reverse=True
        )

        summary = {
            "total_students": len(data),
            "grades_count": grade_count
        }

        return Response({
            "summary": summary,
            "students": data
        })

from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings  # 🔥 muhimu

class SendReportCards(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student_ids = request.data.get("student_ids", [])
        exam_id = request.data.get("exam_id")

        if not student_ids:
            return Response({"error":"No students selected"}, status=400)

        exam = Exam.objects.get(id=exam_id)
        year = request.data.get("year")

        sent_count = 0
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            parent_email = student.parent.email if student.parent else None

            if not parent_email:
                continue

            # ================= EMAIL CONTENT =================
            subject = f"{exam.name} Report Card"

            message = f"Dear {student.parent.first_name},\n\n"
            message += f"Here is the report card for your child {student.first_name} {student.last_name}.\n\n"

            #results = Result.objects.filter(student=student, exam=exam)
            results = Result.objects.filter(
                student=student,
                exam=exam,
                year=year
            )

            total_marks = results.aggregate(total=Sum("marks"))["total"] or 0
            count = results.count()
            average = total_marks / count if count > 0 else 0

            for r in results:
                message += f"{r.subject.name}: {r.marks} ({r.grade})\n"

            message += f"\nTotal Marks: {total_marks}\n"
            message += f"Average: {round(average,2)}\n"
            message += "\nRegards,\nShuleFasta School"

            # ================= SEND EMAIL =================
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # 🔥 HAPA NDIPO FIX
                [parent_email],
                fail_silently=False
            )

            # ================= SAVE =================
            ReportSent.objects.create(
                school=student.school,
                student=student,
                exam=exam,
                sent_by=request.user,
                sent_at=timezone.now()
            )

            sent_count += 1

        return Response({"message":f"Reports sent to {sent_count} students"})



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.db.models import Sum
from io import BytesIO

from .models import Student, Result, Exam
class DownloadAllReportsPDF(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, exam_id, year):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=A4)

        elements = []

        styles = getSampleStyleSheet()

        exam = Exam.objects.get(id=exam_id)

        results = Result.objects.filter(
            classroom_id=class_id,
            exam_id=exam_id,
            year=year,
            school=request.user.school
        )

        student_ids = results.values_list(
            "student_id",
            flat=True
        ).distinct()

        students = Student.objects.filter(
            id__in=student_ids
        )

        for index, student in enumerate(students, start=1):

            student_results = results.filter(
                student=student
            )

            if not student_results.exists():
                continue

            total_marks = student_results.aggregate(
                total=Sum("marks")
            )["total"] or 0

            count = student_results.count()

            avg = total_marks / count if count > 0 else 0

            first_result = student_results.first()

            elements.append(
                Paragraph(
                    f"<b>{index}. {student.first_name} {student.last_name}</b>",
                    styles['Title']
                )
            )

            elements.append(Spacer(1,10))

            elements.append(
                Paragraph(
                    f"Class: {first_result.classroom.name}",
                    styles['Normal']
                )
            )

            elements.append(
                Paragraph(
                    f"Stream: {first_result.stream.name}",
                    styles['Normal']
                )
            )

            elements.append(
                Paragraph(
                    f"Academic Year: {year}",
                    styles['Normal']
                )
            )

            elements.append(
                Paragraph(
                    f"Exam: {exam.name}",
                    styles['Normal']
                )
            )

            elements.append(Spacer(1,10))

            table_data = [["Subject","Marks","Grade"]]

            for r in student_results:

                table_data.append([
                    r.subject.name,
                    r.marks,
                    r.grade
                ])

            table = Table(table_data)

            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.grey),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('GRID',(0,0),(-1,-1),1,colors.black),
            ]))

            elements.append(table)

            elements.append(Spacer(1,10))

            elements.append(
                Paragraph(
                    f"Total: {total_marks}",
                    styles['Normal']
                )
            )

            elements.append(
                Paragraph(
                    f"Average: {round(avg,2)}",
                    styles['Normal']
                )
            )

            elements.append(Spacer(1,30))

        doc.build(elements)

        buffer.seek(0)

        return HttpResponse(
            buffer,
            content_type='application/pdf',
            headers={
                'Content-Disposition':'attachment; filename="all_report_cards.pdf"'
            },
        )









######################### UPDATES AND DELETE VIEWS #######################################

class UpdateDeleteStudent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        student = Student.objects.get(id=pk, school=request.user.school)
        serializer = StudentSerializer(student, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        student = Student.objects.get(id=pk, school=request.user.school)
        student.delete()
        return Response({"message": "Deleted"})





class StudentSubjectResults(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_id = request.GET.get("student_id")
        exam_id = request.GET.get("exam_id")

        results = Result.objects.filter(
            student_id=student_id,
            exam_id=exam_id,
            school=request.user.school
        )

        data = []

        for r in results:
            data.append({
                "result_id": r.id,
                "subject_name": r.subject.name,
                "marks": r.marks
            })

        return Response(data)

class UpdateDeleteResult(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            result = Result.objects.get(id=pk, school=request.user.school)
        except Result.DoesNotExist:
            return Response({"error": "Result not found"})

        serializer = ResultSerializer(result, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            result = Result.objects.get(id=pk, school=request.user.school)
        except Result.DoesNotExist:
            return Response({"error": "Result not found"})

        result.delete()
        return Response({"message": "Result deleted"})












###########################  NEW ##########################################################################





# class PromoteStudentsView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         current_year = request.data.get("current_year")

#         if not current_year:
#             return Response({
#                 "error":"Current year is required"
#             }, status=400)

#         current_year = int(current_year)

#         next_year = current_year + 1

#         school = request.user.school

#         enrollments = StudentEnrollment.objects.filter(
#             school=school,
#             year=current_year
#         ).select_related("classroom", "stream", "student")

#         promoted_count = 0

#         skipped_students = []

#         for enrollment in enrollments:

#             current_class = enrollment.classroom

#             current_name = current_class.name.lower().strip()

#             next_class_name = None

#             # =========================
#             # PRIMARY
#             # =========================

#             if current_name == "grade 1":
#                 next_class_name = "Grade 2"

#             elif current_name == "grade 2":
#                 next_class_name = "Grade 3"

#             elif current_name == "grade 3":
#                 next_class_name = "Grade 4"

#             elif current_name == "grade 4":
#                 next_class_name = "Grade 5"

#             elif current_name == "grade 5":
#                 next_class_name = "Grade 6"

#             elif current_name == "grade 6":
#                 next_class_name = "Grade 7"

#             # =========================
#             # SECONDARY
#             # =========================

#             elif current_name == "form 1":
#                 next_class_name = "Form 2"

#             elif current_name == "form 2":
#                 next_class_name = "Form 3"

#             elif current_name == "form 3":
#                 next_class_name = "Form 4"

#             elif current_name == "form 4":
#                 next_class_name = "Form 5"

#             elif current_name == "form 5":
#                 next_class_name = "Form 6"

#             else:
#                 skipped_students.append({
#                     "student": enrollment.student.first_name,
#                     "reason": "No next class found"
#                 })
#                 continue

#             next_class = ClassRoom.objects.filter(
#                 school=school,
#                 name__iexact=next_class_name
#             ).first()

#             if not next_class:

#                 skipped_students.append({
#                     "student": enrollment.student.first_name,
#                     "reason": f"{next_class_name} does not exist"
#                 })

#                 continue

#             # =========================
#             # CHECK IF ALREADY PROMOTED
#             # =========================

#             exists = StudentEnrollment.objects.filter(
#                 school=school,
#                 student=enrollment.student,
#                 year=next_year
#             ).exists()

#             if exists:

#                 skipped_students.append({
#                     "student": enrollment.student.first_name,
#                     "reason": "Already promoted"
#                 })

#                 continue

#             # =========================
#             # CREATE NEW ENROLLMENT
#             # =========================

#             StudentEnrollment.objects.create(
#                 school=school,
#                 student=enrollment.student,
#                 classroom=next_class,
#                 stream=enrollment.stream,
#                 year=next_year
#             )

#             promoted_count += 1

#         return Response({
#             "message":f"{promoted_count} students promoted successfully",
#             "promoted_count":promoted_count,
#             "next_year":next_year,
#             "skipped_students":skipped_students
#         })




class PromoteStudentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        current_year = request.data.get("current_year")

        if not current_year:
            return Response({"error": "Current year is required"}, status=400)

        current_year = int(current_year)
        next_year = current_year + 1

        school = request.user.school

        enrollments = StudentEnrollment.objects.filter(
            school=school,
            year=current_year
        ).select_related("classroom", "stream", "student")

        promoted_count = 0
        skipped_students = []

        # =========================
        # CLASS MAPPING
        # =========================
        class_map = {
            "grade 1": "Grade 2",
            "grade 2": "Grade 3",
            "grade 3": "Grade 4",
            "grade 4": "Grade 5",
            "grade 5": "Grade 6",
            "grade 6": "Grade 7",
            "form 1": "Form 2",
            "form 2": "Form 3",
            "form 3": "Form 4",
            "form 4": "Form 5",
            "form 5": "Form 6",
        }

        # =========================
        # GROUP COUNTERS (NEW FEATURE)
        # =========================
        promotion_summary = {}

        for enrollment in enrollments:

            current_class = enrollment.classroom
            current_name = current_class.name.lower().strip()

            if current_name not in class_map:
                skipped_students.append({
                    "student": enrollment.student.first_name,
                    "reason": "No next class found"
                })
                continue

            next_class_name = class_map[current_name]

            next_class = ClassRoom.objects.filter(
                school=school,
                name__iexact=next_class_name
            ).first()

            if not next_class:
                skipped_students.append({
                    "student": enrollment.student.first_name,
                    "reason": f"{next_class_name} does not exist"
                })
                continue

            # 🔥 FIXED STREAM LOGIC (IMPORTANT PART)
            next_stream = Stream.objects.filter(
                classroom=next_class,
                name=enrollment.stream.name
            ).first()

            if not next_stream:
                skipped_students.append({
                    "student": enrollment.student.first_name,
                    "reason": f"Stream {enrollment.stream.name} not found in {next_class.name}"
                })
                continue

            exists = StudentEnrollment.objects.filter(
                school=school,
                student=enrollment.student,
                year=next_year
            ).exists()

            if exists:
                skipped_students.append({
                    "student": enrollment.student.first_name,
                    "reason": "Already promoted"
                })
                continue

            # =========================
            # CREATE NEW ENROLLMENT
            # =========================
            StudentEnrollment.objects.create(
                school=school,
                student=enrollment.student,
                classroom=next_class,
                stream=next_stream,   # 🔥 FIX HERE
                year=next_year
            )

            promoted_count += 1

            # =========================
            # SUMMARY GROUPING
            # =========================
            key = f"{current_class.name} → {next_class.name}"

            promotion_summary[key] = promotion_summary.get(key, 0) + 1

        # =========================
        # FINAL RESPONSE
        # =========================
        return Response({
            "message": "Promotion completed successfully",
            "promoted_count": promoted_count,
            "next_year": next_year,
            "summary": promotion_summary,
            "skipped_students": skipped_students
        })





###############################  STUDENT BEHAVIOUR ##############################



# =========================
# CREATE STUDENT BEHAVIOUR
# =========================
class CreateStudentBehaviour(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()
        data['school'] = request.user.school.id

        serializer = StudentBehaviourSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


# =========================
# GET ALL BEHAVIOURS (ADMIN + PARENT FILTER)
# =========================
class GetStudentBehaviours(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # ADMIN / TEACHER → all students in school
        if user.role in ['admin', 'teacher']:
            behaviours = StudentBehaviour.objects.filter(
                school=user.school
            ).order_by('-created')

        # PARENT → only their children
        else:
            behaviours = StudentBehaviour.objects.filter(
                student__parent=user
            ).order_by('-created')

        serializer = StudentBehaviourSerializer(behaviours, many=True)

        return Response(serializer.data)


# =========================
# GET SINGLE STUDENT BEHAVIOUR HISTORY
# =========================
class GetStudentBehaviourHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):

        behaviours = StudentBehaviour.objects.filter(
            student_id=student_id,
            school=request.user.school
        ).order_by('-created')

        serializer = StudentBehaviourSerializer(behaviours, many=True)

        return Response(serializer.data)


# =========================
# GET ALL STUDENTS
# ADMIN → ALL
# TEACHER → ALL
# PARENT → ONLY OWN CHILDREN
# =========================

class GetStudentsBasedOnRole(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # =========================
        # ADMIN + TEACHER
        # =========================
        if user.role in ['admin', 'teacher']:

            students = Student.objects.filter(
                school=user.school
            ).order_by('-id')

        # =========================
        # PARENT
        # =========================
        elif user.role == 'parent':

            students = Student.objects.filter(
                parent=user,
                school=user.school
            ).order_by('-id')

        # =========================
        # SAFETY
        # =========================
        else:

            students = Student.objects.none()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)












# class CreateParentComment(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         data = request.data.copy()
#         data["school"] = request.user.school.id
#         data["parent"] = request.user.id

#         serializer = ParentCommentSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)


# class GetParentComments(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         comments = ParentComment.objects.filter(
#             school=request.user.school
#         ).order_by("-created")

#         serializer = ParentCommentSerializer(comments, many=True)
#         return Response(serializer.data)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.core.mail import send_mail
from django.conf import settings

from .models import ParentComment
from .serializers import ParentCommentSerializer


class CreateParentComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()
        data["school"] = request.user.school.id
        data["parent"] = request.user.id

        serializer = ParentCommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class GetParentComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        comments = ParentComment.objects.filter(
            school=request.user.school
        ).order_by("-created")

        data = []

        for i in comments:

            data.append({
                "id":i.id,
                "comment":i.comment,
                "created":i.created,
                "parent_name":i.parent.username,
                "parent_email":i.parent.email,
            })

        return Response(data)



class SendReplyToParentComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        email = "juniordimoso8@gmail.com" #request.data.get("email")
        message = request.data.get("message")

        if not email:
            return Response({
                "error":"Parent email is required"
            },status=400)

        if not message:
            return Response({
                "error":"Message is required"
            },status=400)

        send_mail(
            subject="Shule Fasta",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return Response({
            "success":"Email sent successfully"
        })








class CreateTeacherScheme(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()
        data["school"] = request.user.school.id

        serializer = TeacherSchemeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response({"errors": serializer.errors}, status=400)



class GetTeacherSchemes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        teacher_id = request.GET.get("teacher")
        term = request.GET.get("term")
        subject_id = request.GET.get("subject")

        schemes = TeacherScheme.objects.filter(
            school=request.user.school
        )

        if teacher_id:
            schemes = schemes.filter(teacher_id=teacher_id)

        if term:
            schemes = schemes.filter(term=term)

        if subject_id:
            schemes = schemes.filter(subject_id=subject_id)

        serializer = TeacherSchemeSerializer(schemes, many=True)
        return Response(serializer.data)







class UpdateDeleteSubject(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            # Tunatafuta somo kwa ID na kuhakikisha ni la shule ya huyu user
            subject = Subject.objects.get(id=pk, school=request.user.school)
        except Subject.DoesNotExist:
            return Response(
                {"detail": "Subject not found or you do not have permission."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Kuedit somo (partial=True inaruhusu kubadili baadhi ya fields bila kulazimisha zote)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            # Tunatafuta somo kwa ID na kuhakikisha ni la shule ya huyu user kabla ya kufuta
            subject = Subject.objects.get(id=pk, school=request.user.school)
            subject.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response(
                {"detail": "Subject not found or you do not have permission."},
                status=status.HTTP_404_NOT_FOUND
            )