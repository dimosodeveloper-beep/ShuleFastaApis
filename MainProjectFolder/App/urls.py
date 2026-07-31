from django.urls import path
from . import views
#register
urlpatterns = [

    path(
        "change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password"
    ),

    path(
        "forgot-password/",
        views.SendOTPView.as_view(),
        name="forgot-password"
    ),

    path(
        "verify-otp/",
        views.VerifyOTPView.as_view(),
        name="verify-otp"
    ),

    path(
        "reset-password/",
        views.ResetPasswordView.as_view(),
        name="reset-password"
    ),




    path(
        'create-academic-year/',
        views.CreateAcademicYear.as_view()
    ),

    path(
        'academic-years/',
        views.GetAcademicYears.as_view()
    ),


    path("dashboard-stats/", views.DashboardStatsView.as_view(), name="dashboard-stats"),

    path('LatestVersionView/', views.LatestVersionView.as_view(), name='LatestVersionView'),

    path('register/', views.RegisterUser.as_view()),

    path('login/', views.LoginUser.as_view()),

    path('create-school/', views.CreateSchool.as_view()),

    path('create-class/', views.CreateClassRoom.as_view()),

    path('classes/', views.GetClasses.as_view()),

    path('create-stream/', views.CreateStream.as_view()),

    path('streams/<int:class_id>/', views.GetStreams.as_view()),

    path('create-student/', views.CreateStudent.as_view()),

    path('students/', views.GetStudents.as_view()),

    path('students_by_class/', views.GetStudents2_By_Class.as_view()),

    path("parents/", views.GetParents.as_view()),
    path("GetTeachersSelectedField/", views.GetTeachersSelectedField.as_view(), name="teachers"),

    #path('students/stream/<int:stream_id>/', views.GetStudentsInStream.as_view()),

    path(
    "students/stream/<int:class_id>/<int:stream_id>/",
    views.GetStudentsInStream.as_view()
    ),

    path(
    "students/stream/<int:class_id>/<int:stream_id>/<int:year>/",
    views.GetStudentsInStream_for_students.as_view()
    ),

    path('get-classrooms/', views.GetClassrooms.as_view()),




    ##########################################################

    path('create-subject/', views.CreateSubject.as_view()),

    path('subjects/', views.GetSubjects.as_view()),

    path('create-exam-category/', views.CreateExamCategory.as_view()),

    path('exam-categories/', views.GetExamCategories.as_view()),

    path('create-exam/', views.CreateExam.as_view()),

    path('exams/', views.GetExams.as_view()),

    ######## NEW RESULTS
    path('exams_results/', views.GetExamsResults.as_view()),
    path('exam_classes/<int:exam_id>/', views.GetExamClasses.as_view()),
    path('students_results/', views.GetStudentsResults.as_view()),
    path('student_results/<int:student_id>/', views.GetSingleStudentResults.as_view()),
    path("results_summary/", views.ResultsSummaryView.as_view()),



    path('add-result/', views.AddResult.as_view()),

    path('bulk-results/', views.BulkResultUpload.as_view()),

    #path('student-results/<int:student_id>/', views.GetStudentResults.as_view()),

    path('exam-results/<int:exam_id>/', views.GetExamResults.as_view()),



    ####################################################################

        path(
        'report-card/<int:student_id>/<int:exam_id>/',
        views.StudentReportCard.as_view()
    ),

    path(
        'class-ranking/<int:class_id>/<int:exam_id>/',
        views.ClassRanking.as_view()
    ),

    path(
        'stream-ranking/<int:stream_id>/<int:exam_id>/',
        views.StreamRanking.as_view()
    ),

    path(
        'top10/<int:class_id>/<int:exam_id>/',
        views.TopStudents.as_view()
    ),




    ######################### ATTENDANCE ##########################

        path(
        'take-attendance/',
        views.TakeAttendance.as_view()
    ),

    path(
        'bulk-attendance/',
        views.BulkAttendance.as_view()
    ),

    path(
        'attendance/<int:class_id>/<int:stream_id>/',
        views.GetAttendanceByDate.as_view()
    ),

    # path(
    #     'stream-attendance-stats/<int:stream_id>/',
    #     views.StreamStudentsAttendanceStats.as_view()
    # ),

    path(
        'student-attendance/<int:student_id>/',
        views.StudentAttendanceHistory.as_view()
    ),

    path(
        'attendance-statistics/<int:student_id>/',
        views.AttendanceStatistics.as_view()
    ),


    #path('stream-attendance-stats/<int:stream_id>/', views.StreamStudentsAttendanceStats.as_view()),
    path(
    'stream-attendance-stats/<int:class_id>/<int:stream_id>/',
    views.StreamStudentsAttendanceStats.as_view()
    ),

    path('attendance-statistics/<int:student_id>/', views.AttendanceStatistics.as_view()),








    #############################################################


    # path(
    #     'promote-student/',
    #     views.PromoteStudent.as_view()
    # ),

    path(
        'promote-class/',
        views.PromoteClass.as_view()
    ),

    path(
        'parent-children/',
        views.ParentChildren.as_view()
    ),

    # urls.py

    path(
        'parent-child-results/<int:student_id>/<int:exam_id>/',
        views.ParentChildResults.as_view()
    ),


    path(
        'report-card-data/<int:student_id>/<int:exam_id>/',
        views.ReportCardData.as_view()
    ),






    ##########################################################

    #     path(
    #     'create-teacher/',
    #     views.CreateTeacher.as_view()
    # ),

    # path(
    #     'teachers/',
    #     views.GetTeachers.as_view()
    # ),

    # path(
    #     'create-fee-structure/',
    #     views.CreateFeeStructure.as_view()
    # ),

    # path(
    #     'fee-structure/',
    #     views.GetFeeStructure.as_view()
    # ),

    # path(
    #     'pay-fee/',
    #     views.PayFee.as_view()
    # ),

    # path(
    #     'student-fee-history/<int:student_id>/',
    #     views.StudentFeeHistory.as_view()
    # ),

    path(
        'school-dashboard/',
        views.SchoolDashboard.as_view()
    ),

    path(
        'fee-dashboard/',
        views.FeeDashboard.as_view()
    ),





    ##########################################################

    path("create-timetable/", views.CreateTimetable.as_view()),
    path("class-timetable/<int:class_id>/", views.ClassTimetable.as_view()),

    path("classes2/", views.GetClasses2.as_view()),
    path("teachers2/", views.GetTeachers2.as_view()),
    path("subjects2/", views.GetSubjects2.as_view()),

    path(
        'generate-report/<int:student_id>/',
        views.GenerateReportCard.as_view()
    ),


    path("create-teacher/", views.CreateTeacher.as_view()),
    path("teachers/", views.GetTeachers.as_view()),
    path("teacher-users/", views.GetTeacherUsers.as_view()),
    path("teacher/<int:id>/", views.GetSingleTeacher.as_view()),

    path("create-event/", views.CreateEventView.as_view()),
    path("events/", views.GetEventsView.as_view()),





    path("create-grading-system/", views.CreateGradingSystem.as_view()),
    path("grading-system/", views.GetGradingSystem.as_view()),
    path("grading-system/<int:pk>/", views.UpdateDeleteGradingSystem.as_view()),


    path('all_report_cards/', views.GetAllReportCards.as_view()),
    path('send_report_cards/', views.SendReportCards.as_view()),
    #path('download_all_reports/<int:class_id>/<int:exam_id>/', views.DownloadAllReportsPDF.as_view()),
    path(
    'download-all-reports-pdf/<int:class_id>/<int:exam_id>/<int:year>/',
    views.DownloadAllReportsPDF.as_view()
    ),




    path("update-delete-student/<int:pk>/", views.UpdateDeleteStudent.as_view()),
    path("update-delete-result/<int:pk>/", views.UpdateDeleteResult.as_view()),
    path("student-subject-results/", views.StudentSubjectResults.as_view()),



    # =========================================
    # FEE STRUCTURE
    # =========================================

    path(
        "create-fee-structure/",
        views.CreateFeeStructure.as_view()
    ),

    path(
        "fee-structures/",
        views.GetFeeStructures.as_view()
    ),


    # =========================================
    # FEE PAYMENT
    # =========================================

    path(
        "create-fee-payment/",
        views.CreateFeePayment.as_view()
    ),

    path(
        "fee-payments/",
        views.GetFeePayments.as_view()
    ),


    # =========================================
    # STUDENT FEE SUMMARY
    # =========================================

    path(
        "student-fee-summary/<int:student_id>/",
        views.GetStudentFeeSummary.as_view()
    ),

    path(
        "all-students-fee-summary/",
        views.GetAllStudentsFeeSummary.as_view()
    ),


    # =========================================
    # PARENT VIEW
    # =========================================

    path(
        "parent-student-fees/",
        views.ParentStudentFeesView.as_view()
    ),

    path("fee-years/", views.GetFeeYears.as_view(), name="fee-years"),

    path("fee-students/<int:year>/", views.GetStudentsByYear.as_view(), name="fee-students"),

    path(
        "student-year-payments/<int:student_id>/<int:year>/",
        views.GetStudentYearPayments.as_view(),
        name="student-year-payments"
    ),


    ################ STUDENTS BEHAVIOUR######################

    path('create-student-behaviour/', views.CreateStudentBehaviour.as_view()),

    path('student-behaviours/', views.GetStudentBehaviours.as_view()),

    path('student-behaviour-history/<int:student_id>/', views.GetStudentBehaviourHistory.as_view()),

    path('students_by_role/', views.GetStudentsBasedOnRole.as_view()),


    path(
    'upload-results-excel/',
    views.UploadResultsExcel.as_view()
    ),


    path(
        'promote-students/',
        views.PromoteStudentsView.as_view()
    ),


    path("parent-comment/create/", views.CreateParentComment.as_view()),
    path("parent-comment/all/", views.GetParentComments.as_view()),
    path("parent-comment/reply/", views.SendReplyToParentComment.as_view()),

    # Student (already existing update only)
    # Teacher Scheme
    path("teacher-scheme/create/", views.CreateTeacherScheme.as_view()),
    path("teacher-scheme/all/", views.GetTeacherSchemes.as_view()),




    path("subjects/<int:pk>/", views.UpdateDeleteSubject.as_view(), name="update-delete-subject"),











]

#CreateResult