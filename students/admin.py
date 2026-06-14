from django.contrib import admin
from .models import User, Student, Competition, Participation, Absence


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'matricule', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email', 'matricule']
    list_editable = ['role']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'matricule', 'first_name_ar', 'last_name_ar',
        'activity', 'category', 'status', 'academic_year', 'created_at'
    ]
    list_filter = ['status', 'category', 'activity', 'academic_year']
    search_fields = ['name', 'matricule', 'first_name_ar', 'last_name_ar', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('معلومات شخصية', {
            'fields': ('name', 'first_name_ar', 'last_name_ar', 'first_name_fr', 'last_name_fr')
        }),
        ('معلومات أكاديمية', {
            'fields': ('matricule', 'specialty', 'academic_year', 'email')
        }),
        ('معلومات إضافية', {
            'fields': ('birth_date', 'birth_place', 'blood')
        }),
        ('النشاط', {
            'fields': ('category', 'activity')
        }),
        ('الملفات', {
            'fields': ('photo', 'schedule')
        }),
        ('الحالة', {
            'fields': ('status', 'created_at')
        }),
    )


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'activity_type', 'activity_name', 'location',
        'start_date', 'end_date', 'status', 'is_travel', 'created_at'
    ]
    list_filter = ['activity_type', 'status', 'is_travel']
    search_fields = ['title', 'location', 'activity_name']
    list_editable = ['status']
    readonly_fields = ['created_at']


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['student', 'competition', 'status', 'responded_at']
    list_filter = ['status']
    search_fields = ['student__name', 'student__matricule', 'competition__title']
    list_editable = ['status']
    readonly_fields = ['responded_at']


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'competition', 'start_date', 'end_date',
        'return_confirmed', 'injury_status', 'return_date'
    ]
    list_filter = ['return_confirmed', 'injury_status', 'is_justified']
    search_fields = ['student__name', 'student__matricule', 'competition__title']
    readonly_fields = ['ai_analyzed_at']
    
    fieldsets = (
        ('معلومات الغياب', {
            'fields': ('student', 'competition', 'start_date', 'end_date')
        }),
        ('تأكيد العودة', {
            'fields': ('return_confirmed', 'return_date', 'is_justified')
        }),
        ('الحالة الصحية', {
            'fields': ('injury_status', 'injury_description')
        }),
        ('تقرير الذكاء الاصطناعي', {
            'fields': ('ai_analysis', 'ai_analyzed_at')
        }),
        ('الصور الطبية', {
            'fields': ('medical_image_1', 'medical_image_2', 'medical_image_3')
        }),
    )