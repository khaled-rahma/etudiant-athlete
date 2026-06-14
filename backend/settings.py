from pathlib import Path
import os
import google.generativeai as genai

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-change-this-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_TZ = True

# ===== ملفات ثابتة ووسائط =====
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===== إعدادات رفع الملفات =====
# زيادة الحد الأقصى لحجم الملفات المرفوعة (لرفع الصور الطبية)
DATA_UPLOAD_MAX_NUMBER_FILES = 10  # عدد الملفات المسموح بها
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100  # عدد الحقول

# الحد الأقصى لحجم الطلب (لرفع صور كبيرة)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# حد حجم الملف الواحد
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# مسارات حفظ الصور الطبية
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'content-type',
    'x-csrftoken',
    'authorization',
]

# استخدام نموذج المستخدم المخصص
AUTH_USER_MODEL = 'students.User'

# رابط تسجيل الدخول
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# ===== Gemini API Configuration =====
GOOGLE_API_KEY = "AIzaSyAkkVVoZc3EDXNY8tS2-xJg2X2K7zNr0TY"
genai.configure(api_key=GOOGLE_API_KEY)

# نموذج Gemini المستخدم لتحليل الصور الطبية
GEMINI_MODEL_NAME = "models/gemini-2.5-flash"  # أو gemini-2.5-flash حسب ما هو متوفر

# إعدادات إضافية للـ API
GEMINI_SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# إعدادات التوليد
GEMINI_GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}