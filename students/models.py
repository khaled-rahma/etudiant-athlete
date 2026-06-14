from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('chef_service',     'رئيس المصلحة'),
        ('chef_departement', 'رئيس القسم'),
        ('vp',               'نائب مدير الجامعة'),
        ('student',          'طالب'),
    ]
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    matricule = models.CharField(max_length=12, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} – {self.get_role_display()}"


class Student(models.Model):
    CATEGORY_CHOICES = [('A', 'رياضي'), ('B', 'ثقافي')]
    STATUS_CHOICES   = [
        ('pending',  'قيد المراجعة'),
        ('approved', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]
    
    # الحقول الجديدة للاسم
    first_name_ar = models.CharField(max_length=100, verbose_name='الاسم (عربي)', blank=True, null=True)
    last_name_ar  = models.CharField(max_length=100, verbose_name='اللقب (عربي)', blank=True, null=True)
    first_name_fr = models.CharField(max_length=100, verbose_name='Nom (Français)', blank=True, null=True)
    last_name_fr  = models.CharField(max_length=100, verbose_name='Prénom (Français)', blank=True, null=True)
    academic_year = models.CharField(max_length=20, verbose_name='السنة الدراسية', blank=True, null=True)
    
    # الحقل القديم للاسم (للتوافق مع الإصدارات السابقة)
    name       = models.CharField(max_length=200)
    matricule  = models.CharField(max_length=12, unique=True)
    email      = models.EmailField(blank=True, null=True)
    birth_date = models.DateField()
    blood      = models.CharField(max_length=5)
    specialty  = models.CharField(max_length=200)
    category   = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    activity   = models.CharField(max_length=100)
    photo      = models.ImageField(upload_to='photos/',    blank=True, null=True)
    schedule   = models.FileField( upload_to='schedules/', blank=True, null=True)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    birth_place = models.CharField(max_length=100, verbose_name='مكان الميلاد', blank=True, null=True)

    class Meta:
        verbose_name        = 'طالب'
        verbose_name_plural = 'الطلبة'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.name} – {self.matricule}'


class Competition(models.Model):
    ACTIVITY_TYPE_CHOICES = [('sport', 'رياضي'), ('culture', 'ثقافي')]
    STATUS_CHOICES = [
        ('draft',     'وارد جديد'),
        ('sent',      'أُرسلت للطلبة'),
        ('completed', 'مكتملة'),
    ]
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE_CHOICES)
    activity_name = models.CharField(max_length=100)
    title         = models.CharField(max_length=200)
    location      = models.CharField(max_length=200)
    start_date    = models.DateField()
    end_date      = models.DateField()
    is_travel     = models.BooleanField(default=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_date} → {self.end_date})"

    @property
    def category(self):
        return 'A' if self.activity_type == 'sport' else 'B'


class Participation(models.Model):
    STATUS_CHOICES = [
        ('pending',  'في الانتظار'),
        ('accepted', 'موافق'),
        ('refused',  'غير موافق'),
    ]
    student      = models.ForeignKey(Student,     on_delete=models.CASCADE, related_name='participations')
    competition  = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='participations')
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'competition']

    def __str__(self):
        return f"{self.student.name} – {self.competition.title}"


class Absence(models.Model):
    HEALTH_CHOICES = [
        ('healthy', 'سليم'),
        ('injured', 'مصاب'),
        ('sick',    'مريض'),
    ]
    student            = models.ForeignKey(Student,     on_delete=models.CASCADE, related_name='absences')
    competition        = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='absences')
    start_date         = models.DateField()
    end_date           = models.DateField()
    is_justified       = models.BooleanField(default=True)
    return_confirmed   = models.BooleanField(default=False)
    return_date        = models.DateTimeField(null=True, blank=True)
    injury_status      = models.CharField(max_length=10, choices=HEALTH_CHOICES, default='healthy')
    injury_description = models.TextField(blank=True)

    # ─── حقول تقرير الذكاء الاصطناعي ───
    ai_analysis        = models.JSONField(null=True, blank=True)   # نتيجة Gemini كاملة
    ai_analyzed_at     = models.DateTimeField(null=True, blank=True)

    # صور التقرير الطبي (حتى 3 صور)
    medical_image_1    = models.ImageField(upload_to='medical_reports/', blank=True, null=True)
    medical_image_2    = models.ImageField(upload_to='medical_reports/', blank=True, null=True)
    medical_image_3    = models.ImageField(upload_to='medical_reports/', blank=True, null=True)

    class Meta:
        unique_together = ['student', 'competition']

    def __str__(self):
        return f"{self.student.name} – {self.start_date} → {self.end_date}"