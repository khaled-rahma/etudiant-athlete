from django.urls import path
from . import views

urlpatterns = [
    # ===== المصادقة =====
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard_page, name='dashboard'),

    # ===== API الطلبة =====
    path('api/register/', views.api_register, name='api_register'),
    path('api/students/', views.api_students, name='api_students'),
    path('api/students/<int:student_id>/status/', views.api_update_status, name='api_update_status'),
    path('api/students/<int:student_id>/delete/', views.api_delete_student, name='api_delete_student'),
    path('api/stats/', views.api_stats, name='api_stats'),

    # ===== المسابقات =====
    path('competitions/add/', views.add_competition, name='add_competition'),
    path('competitions/incoming/', views.incoming_competitions, name='incoming_competitions'),
    path('competitions/receive/<int:competition_id>/', views.receive_competition, name='receive_competition'),
    path('competitions/send/<int:competition_id>/', views.send_competition, name='send_competition'),
    path('competitions/all-results/', views.all_competitions_results, name='all_competitions_results'),
    path('competitions/send-report/<int:competition_id>/', views.send_final_report, name='send_final_report'),

    # ===== الطالب =====
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # ===== APIs المشاركات والعودة =====
    path('api/participation/<int:participation_id>/<str:response>/', views.respond_to_participation, name='respond_to_participation'),
    path('api/confirm-return/', views.api_confirm_return, name='confirm_return'),
    path('api/confirm-return-cultural/', views.api_confirm_return_cultural, name='confirm_return_cultural'),
    path('api/confirm-return-with-analysis/', views.api_confirm_return_with_analysis, name='confirm_return_with_analysis'),

    # ===== الغيابات =====
    path('absences/', views.view_absences, name='absences'),

    # ===== الإقصاء =====
    path('exclusion-warnings/', views.exclusion_warnings, name='exclusion_warnings'),

    # ===== الذكاء الاصطناعي =====
    path('api/analyze-injury-ai/', views.api_analyze_injury_with_ai, name='analyze_injury_ai'),
    path('injury-insights/', views.injury_insights_report, name='injury_insights_report'),

    # ===== APIs رئيس القسم =====
    path('api/absences/', views.api_absences, name='api_absences'),
    path('api/latest-injury/', views.api_latest_injury, name='api_latest_injury'),

    # ✅ URL واحد صحيح لكل نوع — بدون تكرار
    path('api/get-injury-analysis/<int:participation_id>/', views.api_get_injury_analysis, name='api_get_injury_analysis'),
    path('api/get-injury-analysis-by-absence/<int:absence_id>/', views.api_get_injury_analysis_by_absence, name='api_get_injury_analysis_by_absence'),

    # ===== أخرى =====
    path('test/', views.test_page, name='test_page'),
    path('debug-competitions/', views.debug_competitions, name='debug_competitions'),
    path('debug-all/', views.debug_all, name='debug_all'),
]