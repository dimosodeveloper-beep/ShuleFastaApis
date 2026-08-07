from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin




# ==============================
# SCHOOL
# ==============================

# @admin.register(School)
# class SchoolAdmin(ImportExportModelAdmin):
#     list_display = [
#         "id",
#         "name",
#         "name_SW",
#         "location",
#         "location_SW",
#         "created"
#     ]

#     list_filter = [
#         "created",
#         "name"
#     ]

#     search_fields = [
#         "name",
#         "location"
#     ]

#     # 1. Inaficha model isionekane kwenye Dashboard ya Admin kama sio 'owner'
#     def has_module_permission(self, request):
#         if hasattr(request.user, 'role') and request.user.role == 'owner':
#             return True
#         return False

#     # 2. Inazuia kuona list ya data hata kama akijaribu kuandika URL kwa mkono
#     def has_view_permission(self, request, obj=None):
#         return hasattr(request.user, 'role') and request.user.role == 'owner'

#     # 3. Inazuia kuongeza shule
#     def has_add_permission(self, request):
#         return hasattr(request.user, 'role') and request.user.role == 'owner'

#     # 4. Inazuia kubadilisha shule
#     def has_change_permission(self, request, obj=None):
#         return hasattr(request.user, 'role') and request.user.role == 'owner'

#     # 5. Inazuia kufuta shule
#     def has_delete_permission(self, request, obj=None):
#         return hasattr(request.user, 'role') and request.user.role == 'owner'

@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "name",
        "name_SW",
        "location",
        "location_SW",
        "created"
    ]

    list_filter = [
        "created",
        "name"
    ]

    search_fields = [
        "name",
        "location"
    ]



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

# ==============================
# CUSTOMER USER
# ==============================

@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "school",
        "is_staff",
        "is_active"
    ]

    list_filter = [
        "role",
        "school",
        "is_staff",
        "is_active"
    ]

    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name"
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {"fields": ("role", "school", "role_SW")},
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {"fields": ("role", "school", "role_SW")},
        ),
    )

    # # Hatua ya A: Kuchuja orodha (List) ya watumiaji wanaonekana
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)

    #     # Kama mtumiaji ana role ya 'owner', mruhusu aone watumiaji wote
    #     if hasattr(request.user, 'role') and request.user.role == 'owner':
    #         return qs

    #     # Kama siyo owner, mpe watumiaji wa shule yake tu
    #     if request.user.school:
    #         return qs.filter(school=request.user.school)

    #     # Usalama: Kama hana shule na sio owner, asione mtumiaji yeyote
    #     return qs.none()

    # # Hatua ya B: Kuchuja Dropdown ya Shule wakati wa kuongeza/kuhariri mtumiaji
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "school":
    #         if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
    #             if request.user.school:
    #                 kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
    #             else:
    #                 kwargs["queryset"] = db_field.related_model.objects.none()

    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # # Hatua ya C: Kumlazimisha mtumiaji kuwa chini ya shule ya yule aliyemsave
    # def save_model(self, request, obj, form, change):
    #     if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
    #         if request.user.school:
    #             obj.school = request.user.school

    #     super().save_model(request, obj, form, change)


# ==============================
# ACADEMIC YEAR
# ==============================

@admin.register(AcademicYear)
class AcademicYearAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "year",
        "created"
    ]

    list_filter = [
        "year",
        "school",
        "created"
    ]

    search_fields = [
        "year"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya miaka ya masomo
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone miaka yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe miaka ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuingia kwenye shule ya yule aliyem-save
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# ==============================
# CLASSROOM
# ==============================

@admin.register(ClassRoom)
class ClassRoomAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "name",
        "name_SW",
        "created"
    ]

    list_filter = [
        "school",
        "created"
    ]

    search_fields = [
        "name",
        "name_SW"
    ]

    # Hatua ya A: Kuchuja orodha ya madarasa
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ni 'owner', mruhusu aone madarasa yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe madarasa ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya aliyelogin wakati wa ku-save darasa
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# STREAM
# ==============================

@admin.register(Stream)
class StreamAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "name",
        "name_SW",
        "classroom"
    ]

    list_filter = [
        "classroom"
    ]

    search_fields = [
        "name",
        "name_SW"
    ]

    # Hatua ya A: Kuchuja orodha ya mikondo (Streams) kwa kupitia darasa (Classroom)
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe mikondo ya shule yake tu kwa kupitia darasa lake
        if request.user.school:
            return qs.filter(classroom__school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya darasa ili ionyeshe madarasa ya shule yake tu
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "classroom":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    # Inachuja madarasa ambayo yanamilikiwa na shule ya huyo user
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================
# SUBJECT
# ==============================

@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "name",
        "name_SW"
    ]

    list_filter = [
        "school"
    ]

    search_fields = [
        "name",
        "name_SW"
    ]

    # Hatua ya A: Kuchuja orodha ya masomo
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya aliyelogin wakati wa ku-save somo
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)

# ==============================
# STUDENT
# ==============================

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "parent",
        "first_name",
        "last_name",
        "admission_number",
        "gender",
        "created"
    ]

    list_filter = [
        "school",
        "gender",
        "created"
    ]

    search_fields = [
        "first_name",
        "last_name",
        "admission_number"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya wanafunzi wanaonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone wanafunzi wote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe wanafunzi wa shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        # Usalama: Kama hana shule na sio owner, asione mwanafunzi yeyote
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule wakati wa kuongeza mwanafunzi mpya
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            # Kama sio owner, mruhusu kuona shule yake tu kwenye dropdown
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlizimisha mwanafunzi kuingia kwenye shule ya yule aliyem-save
    def save_model(self, request, obj, form, change):
        # Kama sio owner na hajachagua shule (au imefichwa), mfumo unaweka shule ya huyo user
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)



# ==============================
# STUDENT ENROLLMENT
# ==============================
# ==============================
# STUDENT ENROLLMENT
# ==============================

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "student",
        "classroom",
        "stream",
        "year",
        "created"
    ]

    list_filter = [
        "school",
        "classroom",
        "stream",
        "year",
        "created"
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "classroom__name",
        "stream__name"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya Enrollments zinazoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone kila kitu
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe enrollments za shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        # Usalama: Kama hana shule na sio owner, asione kitu chochote
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys wakati wa kuandikisha (Enrollment)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Kama sio owner, basi tuchuje dropdown zote zionyeshe data za shule yake tu
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja dropdown ya Shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja dropdown ya Mwanafunzi (Aone wa shule yake tu)
                elif db_field.name == "student":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 3. Kuchuja dropdown ya Darasa (Aone ya shule yake tu)
                elif db_field.name == "classroom":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 4. Kuchuja dropdown ya Mkondo/Stream (Aone ya madarasa ya shule yake tu)
                elif db_field.name == "stream":
                    kwargs["queryset"] = db_field.related_model.objects.filter(classroom__school=request.user.school)
            else:
                # Usalama: Kama hana shule, dropdown zote ziwe tupu
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save
    def save_model(self, request, obj, form, change):
        # Kama sio owner na hajachagua shule, mfumo unaweka shule ya huyo user aliyelogin
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# TEACHER
# ==============================

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "user",
        "phone",
        "created"
    ]

    list_filter = [
        "school",
        "created"
    ]

    search_fields = [
        "user__username",
        "phone"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya walimu wanaonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone walimu wote wa shule zote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe walimu wa shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        # Usalama: Kama hana shule na sio owner, asione mwalimu yeyote
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys wakati wa kuongeza au kuhariri mwalimu
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Kama sio owner, mruhusu kuona data za shule yake tu kwenye dropdowns
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja dropdown ya Shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja dropdown ya User (Mtumiaji aone watumiaji wa shule yake tu)
                elif db_field.name == "user":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                # Usalama: Kama mtumiaji hana shule, dropdown isionyeshe kitu
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya B.2: Kuchuja Dropdown ya ManyToMany (Subjects)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Kama sio owner, mlimishe kuona masomo ya shule yake tu
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school and db_field.name == "subject":
                kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha mwalimu kuingia kwenye shule ya yule aliyem-save
    def save_model(self, request, obj, form, change):
        # Kama sio owner na hajachagua shule (au imefichwa), mfumo unaweka shule ya huyo user aliyelogin
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)



# ==============================
# FEE STRUCTURE
# ==============================

@admin.register(FeeStructure)
class FeeStructureAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "classroom",
        "amount",
        "term",
        "year"
    ]

    list_filter = [
        "school",
        "classroom",
        "term",
        "year"
    ]

    search_fields = [
        "classroom__name",
        "term"
    ]

    # Hatua ya A: Kuchuja orodha ya muundo wa ada unaoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone ada zote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe muundo wa ada wa shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja dropdown ya Shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja dropdown ya Darasa (Aone ya shule yake tu)
                elif db_field.name == "classroom":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# FEE PAYMENT
# ==============================

@admin.register(FeePayment)
class FeePaymentAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "student",
        "amount_paid",
        "payment_date",
        "term",
        "year",
        "created"
    ]

    list_filter = [
        "school",
        "term",
        "year",
        "payment_date",
        "created"
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "term"
    ]

    # Hatua ya A: Kuchuja orodha ya malipo ya ada yanayoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone malipo yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe malipo ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja dropdown ya Shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja dropdown ya Mwanafunzi (Aone wa shule yake tu)
                elif db_field.name == "student":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)



# ==============================
# EXAM CATEGORY
# ==============================

@admin.register(ExamCategory)
class ExamCategoryAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "name",
        "name_SW"
    ]

    list_filter = [
        "school"
    ]

    search_fields = [
        "name",
        "name_SW"
    ]

    # Hatua ya A: Kuchuja orodha ya kundi la mitihani inayonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone makundi yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe makundi ya mitihani ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha mfumo kuweka shule ya user aliyelogin wakati wa ku-save
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# EXAM
# ==============================

@admin.register(Exam)
class ExamAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "category",
        "name",
        "name_SW",
        "date"
    ]

    list_filter = [
        "school",
        "category",
        "date"
    ]

    search_fields = [
        "name",
        "name_SW"
    ]

    # Hatua ya A: Kuchuja orodha ya mitihani inayonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone mitihani yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe mitihani ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys (School na Category)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja category ya mitihani (Ionyeshe za shule yake tu)
                elif db_field.name == "category":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya B.2: Kuchuja uwanja wa Many-to-Many wa Madarasa (classrooms)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "classrooms":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    # Mtumiaji aone madarasa ya shule yake tu kwenye list
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# RESULT
# ==============================

@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "student",
        "classroom",
        "stream",
        "year",
        "exam",
        "subject",
        "marks",
        "grade",
        "created"
    ]

    list_filter = [
        "school",
        "classroom",
        "stream",
        "year",
        "exam",
        "subject",
        "grade",
        "created"
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "subject__name",
        "exam__name"
    ]

    # Hatua ya A: Kuchuja orodha ya matokeo yanayoonekana kwenye chati/list
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone matokeo ya shule zote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe matokeo ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown zote za Foreign Keys ili zionyeshe data za shule husika tu
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja dropdown ya Shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja dropdown ya Mwanafunzi
                elif db_field.name == "student":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 3. Kuchuja dropdown ya Darasa
                elif db_field.name == "classroom":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 4. Kuchuja dropdown ya Mkondo (Stream) - Inaangalia mikondo ya madarasa ya shule hii
                elif db_field.name == "stream":
                    kwargs["queryset"] = db_field.related_model.objects.filter(classroom__school=request.user.school)

                # 5. Kuchuja dropdown ya Mtihani (Exam)
                elif db_field.name == "exam":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 6. Kuchuja dropdown ya Somo (Subject)
                elif db_field.name == "subject":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                # Kama hana shule na sio owner, dropdown zote ziwe tupu kabisa
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save matokeo mapya
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)

# ==============================
# ATTENDANCE
# ==============================

@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "student",
        "classroom",
        "stream",
        "year",
        "date",
        "status",
        "created"
    ]

    list_filter = [
        "school",
        "classroom",
        "stream",
        "year",
        "status",
        "date",
        "created"
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "status"
    ]

    # Hatua ya A: Kuchuja orodha ya mahudhurio yanayoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone mahudhurio yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe mahudhurio ya shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys (School, Student, Classroom, Stream)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja mwanafunzi wa shule yake tu
                elif db_field.name == "student":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 3. Kuchuja madarasa ya shule yake tu
                elif db_field.name == "classroom":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 4. Kuchuja mikondo (streams) inayomilikiwa na madarasa ya shule hii
                elif db_field.name == "stream":
                    kwargs["queryset"] = db_field.related_model.objects.filter(classroom__school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save mahudhurio
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# TIMETABLE
# ==============================

@admin.register(Timetable)
class TimetableAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "classroom",
        "stream",
        "subject",
        "teacher",
        "day",
        "start_time",
        "end_time",
        "created"
    ]

    list_filter = [
        "school",
        "classroom",
        "stream",
        "subject",
        "teacher",
        "day",
        "created"
    ]

    search_fields = [
        "subject__name",
        "teacher__user__username",
        "day"
    ]

    # Hatua ya A: Kuchuja orodha ya ratiba (Timetable) zinazoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone ratiba zote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe ratiba za shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys (School, Classroom, Stream, Subject, Teacher)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja darasa
                elif db_field.name == "classroom":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 3. Kuchuja mkondo (stream)
                elif db_field.name == "stream":
                    kwargs["queryset"] = db_field.related_model.objects.filter(classroom__school=request.user.school)

                # 4. Kuchuja somo (subject)
                elif db_field.name == "subject":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 5. Kuchuja mwalimu (teacher)
                elif db_field.name == "teacher":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save ratiba mpya
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)

# ==============================
# GRADING SYSTEM
# ==============================

@admin.register(GradingSystem)
class GradingSystemAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "grade",
        "grade_SW",
        "min_score",
        "max_score",
        "remark",
        "remark_SW"
    ]

    list_filter = [
        "school",
        "grade"
    ]

    search_fields = [
        "grade",
        "remark"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya mifumo ya madaraja
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuingia kwenye shule yake
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school
        super().save_model(request, obj, form, change)


# ==============================
# SCHOOL EVENT
# ==============================

@admin.register(SchoolEvent)
class SchoolEventAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "title",
        "event_type",
        "start_date",
        "end_date",
        "created"
    ]

    list_filter = [
        "school",
        "event_type",
        "start_date",
        "end_date",
        "created"
    ]

    search_fields = [
        "title",
        "description"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya matukio
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
                if request.user.school:
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                else:
                    kwargs["queryset"] = db_field.related_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuingia kwenye shule yake
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school
        super().save_model(request, obj, form, change)


# ==============================
# REPORT SENT
# ==============================

@admin.register(ReportSent)
class ReportSentAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "student",
        "exam",
        "sent_by",
        "sent_at"
    ]

    list_filter = [
        "school",
        "exam",
        "sent_at"
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "exam__name",
        "sent_by__username"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya ripoti zilizotumwa
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown zote (School, Student, Exam, Sent By) kulingana na shule ya user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                elif db_field.name == "student":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
                elif db_field.name == "exam":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
                elif db_field.name == "sent_by":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuingia kwenye shule yake
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school
        super().save_model(request, obj, form, change)


# ==============================
# STUDENT BEHAVIOUR
# ==============================

@admin.register(StudentBehaviour)
class StudentBehaviourAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "student",
        "title",
        "status",
        "created"
    ]

    list_filter = [
        "school",
        "status",
        "created"
    ]

    search_fields = [
        "student__first_name",
        "student__last_name",
        "title",
        "status"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya tabia za wanafunzi
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule na Wanafunzi
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)
                elif db_field.name == "student":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuingia kwenye shule yake
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school
        super().save_model(request, obj, form, change)


# ==============================
# TEACHER SCHEME
# ==============================

@admin.register(TeacherScheme)
class TeacherSchemeAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "teacher",
        "subject",
        "classroom",
        "stream",
        "term",
        "topic",
        "week",
        "created"
    ]

    list_filter = [
        "school",
        "term",
        "teacher",
        "classroom",
        "stream",
        "created"
    ]

    search_fields = [
        "teacher__user__username",
        "subject__name",
        "classroom__name",
        "stream__name",
        "topic"
    ]

    # Hatua ya A: Kuchuja orodha (List) ya azimio la kazi (Schemes) zinazoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone schemes zote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe schemes za shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown za Foreign Keys (School, Teacher, Subject, Classroom, Stream)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja walimu wa shule hii tu
                elif db_field.name == "teacher":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 3. Kuchuja masomo ya shule hii tu
                elif db_field.name == "subject":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 4. Kuchuja madarasa ya shule hii tu
                elif db_field.name == "classroom":
                    kwargs["queryset"] = db_field.related_model.objects.filter(school=request.user.school)

                # 5. Kuchuja mikondo (streams) inayomilikiwa na madarasa ya shule hii
                elif db_field.name == "stream":
                    kwargs["queryset"] = db_field.related_model.objects.filter(classroom__school=request.user.school)
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save scheme
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)


# ==============================
# PARENT COMMENT
# ==============================

@admin.register(ParentComment)
class ParentCommentAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "school",
        "parent",
        "comment",
        "created"
    ]

    list_filter = [
        "school",
        "created"
    ]

    search_fields = [
        "parent__username",
        "parent__first_name",
        "parent__last_name",
        "comment"
    ]

    # Hatua ya A: Kuchuja orodha ya maoni ya wazazi yanayoonekana
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Kama mtumiaji ana role ya 'owner', mruhusu aone maoni yote
        if hasattr(request.user, 'role') and request.user.role == 'owner':
            return qs

        # Kama siyo owner, mpe maoni ya kwenye shule yake tu
        if request.user.school:
            return qs.filter(school=request.user.school)

        return qs.none()

    # Hatua ya B: Kuchuja Dropdown ya Shule na Mzazi
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                # 1. Kuchuja shule
                if db_field.name == "school":
                    kwargs["queryset"] = db_field.related_model.objects.filter(id=request.user.school.id)

                # 2. Kuchuja wazazi wa shule hii tu waliopo kwenye CustomerUser
                elif db_field.name == "parent":
                    kwargs["queryset"] = db_field.related_model.objects.filter(
                        school=request.user.school,
                        role='parent'
                    )
            else:
                kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Hatua ya C: Kumlazimisha kuweka shule ya yule aliyelogin wakati wa ku-save comment
    def save_model(self, request, obj, form, change):
        if not (hasattr(request.user, 'role') and request.user.role == 'owner'):
            if request.user.school:
                obj.school = request.user.school

        super().save_model(request, obj, form, change)