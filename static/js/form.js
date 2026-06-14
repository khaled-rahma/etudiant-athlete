// ===== Sports & Cultural Activities Registration System =====
// File: form.js

// ===== سلايدر الخلفية =====
var bgImgs = document.querySelectorAll('.bg-slider img');
var bgIdx  = 0;

setInterval(function() {
    bgImgs[bgIdx].classList.remove('active');
    bgImgs[bgIdx].classList.add('leaving');
    var old = bgIdx;
    bgIdx = (bgIdx + 1) % bgImgs.length;
    bgImgs[bgIdx].classList.add('active');
    setTimeout(function() { bgImgs[old].classList.remove('leaving'); }, 1400);
}, 4000);

// ===== تأثير الكتابة =====
var typedEl  = document.getElementById('typed');
var typedTxt = 'نظام تسيير الطالب الرياضي والثقافي – قسم الإعلام الآلي – 2025/2026';
var tIdx = 0, tDel = false;

function runTyped() {
    typedEl.textContent = typedTxt.substring(0, tIdx);
    if (!tDel && tIdx < typedTxt.length)  { tIdx++; setTimeout(runTyped, 70);   }
    else if (tDel && tIdx > 0)             { tIdx--; setTimeout(runTyped, 35);   }
    else { tDel = !tDel; setTimeout(runTyped, tDel ? 2500 : 500); }
}
runTyped();

// ===== معاينة الصورة =====
document.getElementById('photoInput').addEventListener('change', function() {
    var f = this.files[0];
    if (!f) return;
    var r = new FileReader();
    r.onload = function(e) {
        var p = document.getElementById('photoPreview');
        p.src = e.target.result;
        p.style.display = 'block';
        document.getElementById('photoText').style.display = 'none';
    };
    r.readAsDataURL(f);
});

// ===== معاينة الجدول =====
document.getElementById('schedInput').addEventListener('change', function() {
    var f = this.files[0];
    if (!f) return;
    var mb = (f.size / 1024 / 1024).toFixed(2);
    document.getElementById('schedText').innerHTML =
        '<span style="color:#10b981;font-size:0.85rem;">✓ ' +
        f.name + ' (' + mb + ' MB)</span>';
    document.getElementById('schedBox').classList.add('done');
});

// ===== اختيار النشاط =====
document.getElementById('catA').addEventListener('change', function() {
    document.getElementById('sportField').style.display   = 'block';
    document.getElementById('cultureField').style.display = 'none';
    document.getElementById('rcA').classList.add('sel');
    document.getElementById('rcB').classList.remove('sel');
    // تحديث required fields
    document.getElementById('sportSelect').required = true;
    document.getElementById('cultureSelect').required = false;
});

document.getElementById('catB').addEventListener('change', function() {
    document.getElementById('cultureField').style.display = 'block';
    document.getElementById('sportField').style.display   = 'none';
    document.getElementById('rcB').classList.add('sel');
    document.getElementById('rcA').classList.remove('sel');
    // تحديث required fields
    document.getElementById('sportSelect').required = false;
    document.getElementById('cultureSelect').required = true;
});

// ===== ضغط الصورة =====
function compressImage(file, maxW, quality) {
    return new Promise(function(resolve) {
        if (!file.type.startsWith('image/')) {
            resolve(file);
            return;
        }
        var img = new Image();
        var url = URL.createObjectURL(file);
        img.onload = function() {
            URL.revokeObjectURL(url);
            var w = img.width, h = img.height;
            if (w > maxW) { h = Math.round(h * maxW / w); w = maxW; }
            var canvas = document.createElement('canvas');
            canvas.width = w; canvas.height = h;
            canvas.getContext('2d').drawImage(img, 0, 0, w, h);
            canvas.toBlob(function(blob) {
                resolve(new File([blob], file.name, { type: 'image/jpeg' }));
            }, 'image/jpeg', quality);
        };
        img.src = url;
    });
}

function setBar(pct) {
    var bar = document.getElementById('progressBar');
    if (bar) bar.style.width = pct + '%';
}

function showError(msg) {
    var el = document.getElementById('errorMsg');
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
    } else {
        alert(msg);
    }
}

function hideError() {
    var el = document.getElementById('errorMsg');
    if (el) el.style.display = 'none';
}

// ===== إرسال النموذج =====
document.getElementById('myForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    hideError();

    // جلب البيانات الجديدة
    var firstNameAr = document.getElementById('firstNameAr').value.trim();
    var lastNameAr = document.getElementById('lastNameAr').value.trim();
    var firstNameFr = document.getElementById('firstNameFr').value.trim();
    var lastNameFr = document.getElementById('lastNameFr').value.trim();
    var academicYear = document.getElementById('academicYear').value;
    var birthDate = document.getElementById('birthDate').value;
    var birthPlace = document.getElementById('birthPlace').value.trim();  // جديد
    var blood = document.getElementById('blood').value;
    var matricule = document.getElementById('matricule').value.trim();
    var specialty = document.getElementById('specialty').value;
    var catEl = document.querySelector('input[name="cat"]:checked');
    var photoFile = document.getElementById('photoInput').files[0];
    var schedFile = document.getElementById('schedInput').files[0];

    // دمج الاسم الكامل للإرسال إلى الخادم
    var fullName = firstNameAr + ' ' + lastNameAr + ' (' + firstNameFr + ' ' + lastNameFr + ')';

    // التحقق من صحة البيانات
    if (!firstNameAr) { showError('الرجاء إدخال الاسم بالعربية.'); return; }
    if (!lastNameAr) { showError('الرجاء إدخال اللقب بالعربية.'); return; }
    if (!firstNameFr) { showError('الرجاء إدخال الاسم بالفرنسية.'); return; }
    if (!lastNameFr) { showError('الرجاء إدخال اللقب بالفرنسية.'); return; }
    if (!academicYear) { showError('الرجاء اختيار السنة الدراسية.'); return; }
    if (!birthDate) { showError('يرجى تحديد تاريخ الميلاد.'); return; }
    if (!birthPlace) { showError('يرجى تحديد مكان الميلاد.'); return; }  // جديد
    if (!blood) { showError('يرجى اختيار زمرة الدم.'); return; }
    if (!matricule) { showError('يرجى كتابة رقم التسجيل.'); return; }
    if (matricule.length !== 12 || !/^\d+$/.test(matricule)) {
        showError('رقم التسجيل يجب أن يكون 12 رقمًا.');
        return;
    }
    if (!specialty) { showError('يرجى اختيار التخصص الدراسي.'); return; }
    if (!catEl) { showError('يرجى اختيار نوع النشاط.'); return; }
    if (!photoFile) { showError('يرجى رفع الصورة الشخصية.'); return; }
    if (!schedFile) { showError('يرجى رفع الجدول الزمني.'); return; }

    var activity = '';
    if (catEl.value === 'A') {
        activity = document.getElementById('sportSelect').value;
        if (!activity) { showError('يرجى اختيار الرياضة.'); return; }
    } else {
        activity = document.getElementById('cultureSelect').value;
        if (!activity) { showError('يرجى اختيار النشاط الثقافي.'); return; }
    }

    var btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> جاري الإرسال...';
    document.getElementById('progressArea').style.display = 'block';
    setBar(15);

    try {
        // ضغط الصورة قبل الإرسال
        var compressedPhoto = await compressImage(photoFile, 800, 0.82);
        setBar(40);

        // بناء FormData
        var formData = new FormData();
        formData.append('name', fullName);
        formData.append('first_name_ar', firstNameAr);
        formData.append('last_name_ar', lastNameAr);
        formData.append('first_name_fr', firstNameFr);
        formData.append('last_name_fr', lastNameFr);
        formData.append('academic_year', academicYear);
        formData.append('birth_place', birthPlace);  // جديد
        formData.append('matricule', matricule);
        formData.append('email', document.getElementById('email').value.trim());
        formData.append('birth_date', birthDate);
        formData.append('blood', blood);
        formData.append('specialty', specialty);
        formData.append('category', catEl.value);
        formData.append('activity', activity);
        formData.append('photo', compressedPhoto, 'photo.jpg');
        formData.append('schedule', schedFile, schedFile.name);

        // الحصول على CSRF token
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        var token = csrfToken ? csrfToken.value : '';
        setBar(60);

        // إرسال للـ Django
        var response = await fetch('/api/register/', {
            method: 'POST',
            headers: { 'X-CSRFToken': token },
            body: formData,
        });

        setBar(90);
        var result = await response.json();

        if (result.success) {
            setBar(100);
            btn.innerHTML = '✅ تم الإرسال!';
            setTimeout(function() {
                alert('✅ تم إرسال طلبك بنجاح!\nسيظهر لدى رئيس المصلحة في قسم الطلبات الجديدة.');
                window.location.href = '/';
            }, 1000);
        } else {
            throw new Error(result.error || 'حدث خطأ غير معروف');
        }

    } catch(err) {
        showError('❌ ' + (err.message || 'حدث خطأ، يرجى المحاولة مجدداً.'));
        btn.disabled = false;
        btn.innerHTML = '✅ تأكيد وإرسال الطلب';
        document.getElementById('progressArea').style.display = 'none';
        setBar(0);
    }
});

// ===== إضافة CSS للـ spinner =====
var style = document.createElement('style');
style.textContent = `
    .spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid #fff;
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 0.6s linear infinite;
        margin-right: 8px;
        vertical-align: middle;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    #submitBtn:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }
`;
document.head.appendChild(style);