import json as json_module
import json
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Student, User, Competition, Participation, Absence

# ===== Gemini API Service =====
from ml.gemini_service import gemini_service


# ===== صفحات المصادقة =====

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ===== صفحات HTML الرئيسية =====

def register_page(request):
    return render(request, 'register.html')


@login_required
def dashboard_page(request):
    context = {
        'user_role': request.user.role,
        'can_edit': request.user.role == 'chef_service',
        'user_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'dashboard.html', context)


# ===== API: تسجيل طالب جديد =====

@csrf_exempt
@require_http_methods(['POST'])
def api_register(request):
    try:
        # الحقول الجديدة للاسم
        first_name_ar = request.POST.get('first_name_ar', '').strip()
        last_name_ar = request.POST.get('last_name_ar', '').strip()
        first_name_fr = request.POST.get('first_name_fr', '').strip()
        last_name_fr = request.POST.get('last_name_fr', '').strip()
        academic_year = request.POST.get('academic_year', '').strip()
        birth_place = request.POST.get('birth_place', '').strip()  # ← مكان الميلاد جديد
        
        # الحقول القديمة
        name = request.POST.get('name', '').strip()
        matricule = request.POST.get('matricule', '').strip()
        email = request.POST.get('email', '').strip()
        birth_date = request.POST.get('birth_date', '')
        blood = request.POST.get('blood', '')
        specialty = request.POST.get('specialty', '')
        category = request.POST.get('category', '')
        activity = request.POST.get('activity', '').strip().lower()
        photo = request.FILES.get('photo')
        schedule = request.FILES.get('schedule')

        # التحقق من الحقول الإجبارية الجديدة
        if not all([first_name_ar, last_name_ar, first_name_fr, last_name_fr, academic_year, birth_place]):
            return JsonResponse({'success': False, 'error': 'الرجاء ملء جميع حقول الاسم والسنة الدراسية ومكان الميلاد'}, status=400)

        # التحقق من الحقول الإجبارية القديمة
        if not all([name, matricule, birth_date, blood, specialty, category, activity]):
            return JsonResponse({'success': False, 'error': 'All fields are required'}, status=400)

        # التحقق من عدم وجود رقم التسجيل مكرر
        if Student.objects.filter(matricule=matricule).exists():
            return JsonResponse({'success': False, 'error': 'Registration number already exists'}, status=400)

        # إنشاء الطالب الجديد
        student = Student.objects.create(
            name=name,
            first_name_ar=first_name_ar,
            last_name_ar=last_name_ar,
            first_name_fr=first_name_fr,
            last_name_fr=last_name_fr,
            academic_year=academic_year,
            birth_place=birth_place,  # ← حفظ مكان الميلاد
            matricule=matricule,
            email=email,
            birth_date=birth_date,
            blood=blood,
            specialty=specialty,
            category=category,
            activity=activity,
            photo=photo,
            schedule=schedule,
            status='pending'
        )

        return JsonResponse({'success': True, 'message': 'Request sent successfully', 'student_id': student.id})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ===== API: جلب كل الطلبة =====
@require_http_methods(['GET'])
def api_students(request):
    students = Student.objects.all()
    data = []
    for s in students:
        data.append({
            'id': s.id,
            'name': s.name,
            'first_name_ar': s.first_name_ar,
            'last_name_ar': s.last_name_ar,
            'first_name_fr': s.first_name_fr,
            'last_name_fr': s.last_name_fr,
            'academic_year': s.academic_year,
            'birth_date': str(s.birth_date),
            'birth_place': s.birth_place,  # ← أضف هذا السطر
            'matricule': s.matricule,
            'specialty': s.specialty,
            'category': s.category,
            'activity': s.activity,
            'photo': s.photo.url if s.photo else '',
            'schedule': s.schedule.url if s.schedule else '',
            'status': s.status,
            'created_at': s.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    return JsonResponse({'success': True, 'students': data})


# ===== API: تغيير حالة طالب =====

@csrf_exempt
@require_http_methods(['POST'])
def api_update_status(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        body = json.loads(request.body)
        status = body.get('status')
        
        if status not in ['approved', 'rejected', 'pending']:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        
        if status == 'approved' and not User.objects.filter(username=student.matricule).exists():
            from django.contrib.auth.hashers import make_password
            user = User.objects.create(
                username=student.matricule,
                first_name=student.name.split()[0] if ' ' in student.name else student.name,
                last_name=student.name.split()[-1] if ' ' in student.name else '',
                role='student',
                password=make_password(student.matricule)
            )
        
        student.status = status
        student.save()
        
        return JsonResponse({'success': True, 'message': 'Status updated'})
        
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)


@csrf_exempt
@require_http_methods(['DELETE'])
def api_delete_student(request, student_id):
    try:
        Student.objects.get(id=student_id).delete()
        return JsonResponse({'success': True, 'message': 'Student deleted'})
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)


@require_http_methods(['GET'])
def api_stats(request):
    return JsonResponse({
        'success': True,
        'total': Student.objects.filter(status='approved').count(),
        'pending': Student.objects.filter(status='pending').count(),
        'sports': Student.objects.filter(status='approved', category='A').count(),
        'culture': Student.objects.filter(status='approved', category='B').count(),
    })


# ===== المسابقات =====

# ===== المسابقات =====
def add_competition(request):
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type')
        activity_name = request.POST.get('activity_name', '').strip().lower()
        
        Competition.objects.create(
            activity_type=activity_type,
            activity_name=activity_name,
            title=request.POST.get('title'),
            location=request.POST.get('location'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            is_travel=request.POST.get('is_travel') == 'on',
            status='draft'
        )
        
        messages.success(request, '✅ Competition sent successfully to the university')
        # ❌ حذف سطر redirect
        # ✅ إعادة نفس الصفحة مع رسالة نجاح
        return render(request, 'competitions/add.html')
    
    return render(request, 'competitions/add.html')


@login_required
def incoming_competitions(request):
    if request.user.role != 'chef_service':
        return redirect('dashboard')
    
    competitions = Competition.objects.filter(status='draft').order_by('-created_at')
    
    print(f"=== INCOMING COMPETITIONS ===")
    print(f"Total draft competitions: {competitions.count()}")
    for comp in competitions:
        print(f"  - {comp.title} | Type: {comp.activity_type} | Name: '{comp.activity_name}'")
    
    return render(request, 'competitions/incoming.html', {'competitions': competitions})
@login_required
def receive_competition(request, competition_id):
    if request.user.role != 'chef_service':
        return redirect('dashboard')
    
    competition = Competition.objects.get(id=competition_id, status='draft')
    
    if request.method == 'POST':
        competition.status = 'sent'
        competition.save()
        return redirect('send_competition', competition_id=competition.id)
    
    from django.db.models import Q

    students_count = Student.objects.filter(
        category=('A' if competition.activity_type == 'sport' else 'B'),
        status='approved'
    ).filter(
        Q(activity__iexact=competition.activity_name) |
        Q(activity__icontains=competition.activity_name)
    ).count()

    return render(request, 'competitions/receive.html', {
        'competition': competition,
        'students_count': students_count
    })
@login_required
def send_competition(request, competition_id):
    if request.user.role != 'chef_service':
        return redirect('dashboard')
    
    competition = Competition.objects.get(id=competition_id)
    
    from django.db.models import Q
    
    # ✅ بحث متقدم: غير حساس لحالة الحروف ويحتوي على النص
    students = Student.objects.filter(
        category=('A' if competition.activity_type == 'sport' else 'B'),
        status='approved'
    ).filter(
        Q(activity__iexact=competition.activity_name) |  # تطابق تام غير حساس
        Q(activity__icontains=competition.activity_name)   # أو يحتوي على النص
    )
    
    # للتصحيح: اطبع في console
    print(f"=== DEBUG SEND ===")
    print(f"Competition: {competition.title}")
    print(f"Activity name: '{competition.activity_name}'")
    print(f"Students found: {students.count()}")
    for s in students:
        print(f"  - Student: {s.name}, Activity: '{s.activity}'")
    
    if request.method == 'POST':
        for student in students:
            Participation.objects.get_or_create(
                student=student,
                competition=competition,
                defaults={'status': 'pending'}
            )
        
        competition.status = 'sent'
        competition.save()
        messages.success(request, f'✅ Invitations sent to {students.count()} students')
        return redirect('all_competitions_results')
    
    return render(request, 'competitions/send.html', {
        'competition': competition,
        'students': students,
        'students_count': students.count()
    })
@login_required
def all_competitions_results(request):
    # ✅ السماح للأدوار الثلاثة: رئيس المصلحة، رئيس القسم، نائب المدير
    if request.user.role not in ['chef_service', 'chef_departement', 'vp']:
        return redirect('dashboard')
    
    competitions = Competition.objects.all().order_by('-created_at')
    
    competitions_data = []
    for comp in competitions:
        accepted = Participation.objects.filter(competition=comp, status='accepted').count()
        refused = Participation.objects.filter(competition=comp, status='refused').count()
        pending = Participation.objects.filter(competition=comp, status='pending').count()
        
        competitions_data.append({
            'competition': comp,
            'accepted_count': accepted,
            'refused_count': refused,
            'pending_count': pending,
            'total': accepted + refused + pending,
        })
    
    context = {
        'competitions_data': competitions_data,
        'user_role': request.user.role,
    }
    return render(request, 'competitions/all_results.html', context)

@login_required
def send_final_report(request, competition_id):
    if request.user.role != 'chef_service':
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            # ✅ أزل قيد الحالة — اقبل أي مسابقة
            comp = Competition.objects.get(id=competition_id)
            accepted = comp.participations.filter(status='accepted').select_related('student')

            count = 0
            for p in accepted:
                absence, created = Absence.objects.get_or_create(
                    student=p.student,
                    competition=comp,
                    defaults={
                        'start_date':       comp.start_date,
                        'end_date':         comp.end_date,
                        'return_confirmed': False,
                        'injury_status':    'healthy',
                        'is_justified':     True,
                    }
                )
                if created:
                    count += 1

            comp.status = 'completed'
            comp.save()
            messages.success(request, f'✅ Report sent — {count} absence records created for {comp.title}')

        except Competition.DoesNotExist:
            messages.error(request, 'Competition not found')

    return redirect('all_competitions_results')


# ===== واجهة الطالب =====

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(matricule=request.user.username)
    except Student.DoesNotExist:
        return redirect('dashboard')
    
    today = date.today()
    
    pending_parts = Participation.objects.filter(
        student=student, status='pending'
    ).select_related('competition')
    
    accepted_parts = Participation.objects.filter(
        student=student, status='accepted'
    ).select_related('competition')
    
    for part in accepted_parts:
        try:
            absence = Absence.objects.get(competition=part.competition, student=student)
            part.absence_status = absence
        except Absence.DoesNotExist:
            part.absence_status = None
    
    refused_parts = Participation.objects.filter(
        student=student, status='refused'
    ).select_related('competition')
    
    context = {
        'student': student,
        'pending_parts': pending_parts,
        'accepted_parts': accepted_parts,
        'refused_parts': refused_parts,
        'today': today,
    }
    return render(request, 'student/dashboard.html', context)


@csrf_exempt
def respond_to_participation(request, participation_id, response):
    try:
        student = Student.objects.get(matricule=request.user.username)
        participation = Participation.objects.get(id=participation_id, student=student, status='pending')
        
        if response == 'accept':
            participation.status = 'accepted'
        else:
            participation.status = 'refused'
        
        participation.responded_at = timezone.now()
        participation.save()
        
        return JsonResponse({'success': True, 'message': 'Your response has been recorded'})
        
    except (Student.DoesNotExist, Participation.DoesNotExist) as e:
        return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ===== تأكيد العودة =====

@csrf_exempt
@require_http_methods(['POST'])
def api_confirm_return(request):
    """تأكيد العودة للطلاب الرياضيين (مع إمكانية تسجيل إصابة)"""
    try:
        data = json.loads(request.body)
        participation_id = data.get('participation_id')
        injury_status = data.get('injury_status', 'healthy')
        
        student = Student.objects.get(matricule=request.user.username)
        participation = Participation.objects.get(id=participation_id, student=student, status='accepted')
        
        absence, created = Absence.objects.get_or_create(
            student=student,
            competition=participation.competition,
            defaults={
                'start_date': participation.competition.start_date,
                'end_date': participation.competition.end_date,
                'return_confirmed': True,
                'return_date': timezone.now(),
                'injury_status': injury_status,
                'is_justified': True
            }
        )
        
        if not created:
            absence.return_confirmed = True
            absence.return_date = timezone.now()
            absence.injury_status = injury_status
            absence.save()
        
        return JsonResponse({'success': True, 'message': 'Return confirmed successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_confirm_return_cultural(request):
    """تأكيد العودة للطلاب الثقافيين (بدون إصابات)"""
    try:
        data = json.loads(request.body)
        participation_id = data.get('participation_id')
        
        student = Student.objects.get(matricule=request.user.username)
        participation = Participation.objects.get(id=participation_id, student=student, status='accepted')
        
        # التأكد أن الطالب ثقافي
        if student.category != 'B':
            return JsonResponse({'success': False, 'error': 'هذه الخاصية مخصصة للطلاب الثقافيين فقط'}, status=400)
        
        absence, created = Absence.objects.get_or_create(
            student=student,
            competition=participation.competition,
            defaults={
                'start_date': participation.competition.start_date,
                'end_date': participation.competition.end_date,
                'return_confirmed': True,
                'return_date': timezone.now(),
                'injury_status': 'healthy',
                'is_justified': True
            }
        )
        
        if not created:
            absence.return_confirmed = True
            absence.return_date = timezone.now()
            absence.injury_status = 'healthy'
            absence.save()
        
        return JsonResponse({'success': True, 'message': 'تم تأكيد العودة بنجاح'})
        
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Participation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Participation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_confirm_return_with_analysis(request):
    """Confirm return and save AI analysis report (للطلاب الرياضيين فقط)"""
    try:
        data = json.loads(request.body)
        participation_id = data.get('participation_id')
        injury_status = data.get('injury_status', 'injured')
        analysis_data = data.get('analysis_data', {})
        
        student = Student.objects.get(matricule=request.user.username)
        participation = Participation.objects.get(id=participation_id, student=student, status='accepted')
        
        # التأكد أن الطالب رياضي
        if student.category != 'A':
            return JsonResponse({'success': False, 'error': 'AI analysis is only available for sports students'}, status=400)
        
        analysis_json = json.dumps(analysis_data, ensure_ascii=False)
        
        absence, created = Absence.objects.get_or_create(
            student=student,
            competition=participation.competition,
            defaults={
                'start_date': participation.competition.start_date,
                'end_date': participation.competition.end_date,
                'return_confirmed': True,
                'return_date': timezone.now(),
                'injury_status': injury_status,
                'injury_description': analysis_data.get('injury_description', ''),
                'ai_analysis_report': analysis_json,
                'is_justified': True
            }
        )
        
        if not created:
            absence.return_confirmed = True
            absence.return_date = timezone.now()
            absence.injury_status = injury_status
            absence.injury_description = analysis_data.get('injury_description', '')
            absence.ai_analysis_report = analysis_json
            absence.save()
        
        return JsonResponse({'success': True, 'message': 'Return confirmed and report saved successfully'})
        
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Participation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Participation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ===== واجهة رئيس القسم ونائب المدير =====

def view_absences(request):
    if request.user.role not in ['chef_departement', 'vp', 'chef_service']:
        return redirect('dashboard')

    absences = Absence.objects.select_related('student', 'competition').all().order_by('-start_date')

    total         = absences.count()
    returned      = absences.filter(return_confirmed=True).count()
    not_returned  = absences.filter(return_confirmed=False).count()
    injured       = absences.filter(injury_status='injured').count()

    stats = {
        'total':        total,
        'returned':     returned,
        'not_returned': not_returned,  # ✅ مباشرة من الجدول بدون طرح
        'injured':      injured,
    }

    context = {
        'absences':  absences,
        'stats':     stats,
        'user_role': request.user.role,
    }
    return render(request, 'absences/list.html', context)


# ===== نظام الإقصاء =====

def check_exclusion_warning(student):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    unjustified_absences = Absence.objects.filter(
        student=student,
        is_justified=False,
        start_date__gte=thirty_days_ago
    ).count()
    
    return unjustified_absences >= 5


@login_required
def exclusion_warnings(request):
    if request.user.role != 'chef_departement':
        return redirect('dashboard')
    
    students = Student.objects.filter(status='approved')
    warning_students = []
    
    for student in students:
        if check_exclusion_warning(student):
            absences = Absence.objects.filter(
                student=student,
                is_justified=False
            ).order_by('-start_date')
            
            warning_students.append({
                'student': student,
                'absences_count': absences.count(),
                'absences': absences,
            })
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            absences = Absence.objects.filter(
                student=student,
                is_justified=False
            ).order_by('-start_date')[:5]
            
            for absence in absences:
                absence.is_justified = True
                absence.save()
            
            messages.success(request, f'✅ Exclusion cancelled for student {student.name}')
        except Student.DoesNotExist:
            messages.error(request, 'An error occurred')
        
        return redirect('exclusion_warnings')
    
    context = {
        'warning_students': warning_students,
    }
    return render(request, 'exclusion_warnings.html', context)


# ===== صفحة اختبار =====

def test_page(request):
    return HttpResponse("Page is working!")


# ===== الذكاء الاصطناعي (Gemini API) =====

@csrf_exempt
@require_http_methods(['POST'])
def api_analyze_injury_with_ai(request):
    """
    Accepts multipart/form-data:
      - participation_id (required)
      - injury_description (optional text)
      - medical_image_1, medical_image_2, medical_image_3 (optional images)
    """
    try:
        student = Student.objects.get(matricule=request.user.username)

        participation_id   = request.POST.get('participation_id')
        injury_description = request.POST.get('injury_description', '').strip()

        participation = Participation.objects.get(
            id=participation_id, student=student, status='accepted'
        )

        # ── جمع الصور ──
        image_bytes_list = []
        for field in ['medical_image_1', 'medical_image_2', 'medical_image_3']:
            img = request.FILES.get(field)
            if img:
                image_bytes_list.append(img.read())

        # يجب أن يكون هناك نص أو صورة على الأقل
        if not injury_description and not image_bytes_list:
            return JsonResponse(
                {'success': False, 'error': 'Please provide a description or at least one medical image.'},
                status=400
            )

        # ── استدعاء Gemini ──
        analysis = gemini_service.analyze_injury(
            student_name=student.name,
            student_activity=student.activity,
            injury_description=injury_description,
            image_bytes_list=image_bytes_list if image_bytes_list else None,
        )

        if not analysis['success']:
            return JsonResponse({'success': False, 'error': analysis['error']}, status=400)

        # ── حفظ في قاعدة البيانات ──
        absence, _ = Absence.objects.get_or_create(
            student=student,
            competition=participation.competition,
            defaults={
                'start_date': participation.competition.start_date,
                'end_date':   participation.competition.end_date,
            }
        )

        absence.return_confirmed   = True
        absence.return_date        = timezone.now()
        absence.injury_status      = 'injured'
        absence.injury_description = injury_description
        absence.ai_analysis        = analysis['data']
        absence.ai_analyzed_at     = timezone.now()

        # حفظ الصور إن وُجدت
        images = [request.FILES.get(f) for f in
                  ['medical_image_1', 'medical_image_2', 'medical_image_3']]
        if images[0]: absence.medical_image_1 = images[0]
        if images[1]: absence.medical_image_2 = images[1]
        if images[2]: absence.medical_image_3 = images[2]

        absence.save()

        return JsonResponse({
            'success':  True,
            'message':  'Analysis complete',
            'analysis': analysis['data'],
        })

    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Participation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Participation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def injury_insights_report(request):
    if request.user.role != 'chef_departement':
        return redirect('dashboard')

    injuries = Absence.objects.filter(
        injury_status='injured'
    ).select_related('student', 'competition')

    injuries_data = [{
        'student_name':     inj.student.name,
        'student_activity': inj.student.activity,
        'competition':      inj.competition.title,
        'description':      inj.injury_description,
        'date':             str(inj.return_date),
    } for inj in injuries]

    ai_report = 'No injury data available.'
    if injuries_data:
        result = gemini_service.generate_report_for_chef(injuries_data)
        ai_report = result['report'] if result['success'] else result['error']

    return render(request, 'ml/injury_insights.html', {
        'injuries_count': len(injuries_data),
        'ai_report':      ai_report,
        'injuries':       injuries,
    })


# ===== APIs لرئيس القسم =====

@login_required
def api_absences(request):
    absences = Absence.objects.select_related('student', 'competition').order_by('-start_date')
    data = [{
        'id':               a.id,
        'student_name':     a.student.name,
        'student_matricule': a.student.matricule,
        'student_specialty': a.student.specialty,
        'activity':         a.student.activity,
        'competition':      a.competition.title,
        'start_date':       str(a.start_date),
        'end_date':         str(a.end_date),
        'is_travel':        a.competition.is_travel,
        'return_confirmed': a.return_confirmed,
        'injury_status':    a.injury_status,
        'has_ai_report':    bool(a.ai_analysis),
    } for a in absences]
    return JsonResponse({'success': True, 'absences': data})


@login_required
def api_latest_injury(request):
    try:
        latest_absence = Absence.objects.filter(
            injury_status='injured',
            injury_description__isnull=False
        ).exclude(injury_description='').order_by('-return_date').first()
        
        if not latest_absence:
            return JsonResponse({
                'success': False,
                'error': 'No injury records found'
            }, status=404)
        
        analysis = {
            'injury_type': 'Musculoskeletal Injury',
            'affected_body_part': 'Based on description',
            'severity_percentage': 45,
            'severity_level': 'moderate',
            'rest_days': 5,
            'rehab_exercises': ['Rest', 'Ice compress', 'Gentle stretching', 'Elevation'],
            'nutrition_advice': 'Stay hydrated, eat protein-rich foods for tissue repair',
            'light_training_return_days': 3,
            'full_return_days': 7,
            'emergency_warnings': [],
            'recommendation_summary': 'Continue with prescribed treatment. Avoid strenuous activity for 5 days.',
            'student_name': latest_absence.student.name,
            'student_activity': latest_absence.student.activity,
        }
        
        return JsonResponse({'success': True, 'analysis': analysis})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def api_get_injury_analysis(request, participation_id):
    try:
        participation = Participation.objects.select_related(
            'student', 'competition'
        ).get(id=participation_id)

        absence = Absence.objects.get(
            student=participation.student,
            competition=participation.competition,
        )

        if not absence.ai_analysis:
            return JsonResponse({'success': False, 'error': 'No AI analysis found'}, status=404)

        images = []
        for field in ['medical_image_1', 'medical_image_2', 'medical_image_3']:
            img = getattr(absence, field)
            if img:
                images.append(img.url)

        return JsonResponse({
            'success':      True,
            'analysis':     absence.ai_analysis,
            'analyzed_at':  str(absence.ai_analyzed_at),
            'description':  absence.injury_description,
            'images':       images,
            'student_name': absence.student.name,
            'activity':     absence.student.activity,
        })

    except (Participation.DoesNotExist, Absence.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def api_get_injury_analysis_by_absence(request, absence_id):
    try:
        absence = Absence.objects.select_related('student', 'competition').get(id=absence_id)

        if not absence.ai_analysis:
            return JsonResponse({'success': False, 'error': 'No AI analysis for this absence'}, status=404)

        images = []
        for field in ['medical_image_1', 'medical_image_2', 'medical_image_3']:
            img = getattr(absence, field)
            if img:
                images.append(img.url)

        return JsonResponse({
            'success':      True,
            'analysis':     absence.ai_analysis,
            'analyzed_at':  str(absence.ai_analyzed_at),
            'description':  absence.injury_description,
            'images':       images,
            'student_name': absence.student.name,
            'activity':     absence.student.activity,
        })

    except Absence.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Absence not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
@login_required
def debug_competitions(request):
    if request.user.role != 'chef_service':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    competitions = Competition.objects.all().values('id', 'title', 'activity_type', 'activity_name', 'status')
    
    return JsonResponse({
        'count': competitions.count(),
        'competitions': list(competitions)
    })
@login_required
def debug_all(request):
    competitions = Competition.objects.all()
    data = []
    for comp in competitions:
        data.append({
            'id': comp.id,
            'title': comp.title,
            'activity_type': comp.activity_type,
            'activity_name': comp.activity_name,
            'status': comp.status,
        })
    return JsonResponse({'competitions': data, 'count': len(data)})