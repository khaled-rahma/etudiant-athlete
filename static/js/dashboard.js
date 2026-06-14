// ===== صلاحيات =====
var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]')
                    ? document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                    : '';
var CAN_EDIT   = (document.getElementById('can-edit')  || {}).innerText === 'true';
var USER_ROLE  = (document.getElementById('user-role') || {}).innerText || '';

// ===== التنقل =====
function goSection(id, liEl) {
    document.querySelectorAll('.sec').forEach(function(s) { s.style.display = 'none'; });
    var target = document.getElementById(id);
    if (target) target.style.display = 'block';
    document.querySelectorAll('.sidebar li').forEach(function(l) { l.classList.remove('active'); });
    if (liEl) liEl.classList.add('active');
}

// ===== متغيرات =====
var allStudents = [];

// ===== تحميل البيانات =====
function loadData() {
    fetch('/api/students/')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (!data.success) return;
            allStudents = data.students;
            renderAll();
        })
        .catch(function(e) { console.error(e); });

    fetch('/api/stats/')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (!data.success) return;
            setText('stTotal',   data.total);
            setText('stPending', data.pending);
            setText('stSports',  data.sports);
            setText('stCulture', data.culture);
            if (document.getElementById('badgePending'))
                document.getElementById('badgePending').textContent = data.pending;
        });
}

function setText(id, val) {
    var el = document.getElementById(id);
    if (el) el.textContent = val;
}

// ===== رسم الجداول =====
function renderAll() {
    var pending  = allStudents.filter(function(u) { return u.status === 'pending';  });
    var approved = allStudents.filter(function(u) { return u.status === 'approved'; });
    var sports   = approved.filter(function(u) { return u.category === 'A'; });
    var culture  = approved.filter(function(u) { return u.category === 'B'; });

    // طلبات معلقة
    var pTb = document.getElementById('pendingTbody');
    if (pTb) {
        pTb.innerHTML = '';
        pending.forEach(function(u, i) {
            var btns = CAN_EDIT
                ? '<button class="btn-ok" onclick="approveUser(' + u.id + ')"><i class="fas fa-check"></i> قبول</button> ' +
                  '<button class="btn-no" onclick="rejectUser(' + u.id + ')"><i class="fas fa-times"></i> رفض</button>'
                : '<span style="color:#64748b;font-size:0.8rem;">⏳ قيد المراجعة</span>';
            pTb.innerHTML += row5(i+1, u.name, u.specialty, badge(u), btns);
        });
        var emp = document.getElementById('pendingEmpty');
        if (emp) emp.style.display = pending.length === 0 ? 'flex' : 'none';
    }

    // رياضيون
    var sTb = document.getElementById('sportsTbody');
    if (sTb) {
        sTb.innerHTML = '';
        sports.forEach(function(u, i) {
            sTb.innerHTML += row4(i+1,
                '<span class="nm" onclick="openCard('+u.id+')">' + u.name + '</span>',
                u.specialty, badge(u));
        });
    }

    // ثقافيون
    var cTb = document.getElementById('cultureTbody');
    if (cTb) {
        cTb.innerHTML = '';
        culture.forEach(function(u, i) {
            cTb.innerHTML += row4(i+1,
                '<span class="nm" onclick="openCard('+u.id+')">' + u.name + '</span>',
                u.specialty, badge(u));
        });
    }

    // جداول زمنية
    var scTb = document.getElementById('schedTbody');
    if (scTb) {
        scTb.innerHTML = '';
        approved.forEach(function(u, i) {
            scTb.innerHTML += row5(i+1, u.name, u.specialty, badge(u),
                '<button class="btn-sch" onclick="openSched('+u.id+')"><i class="fas fa-eye"></i> عرض</button>');
        });
    }

    // فلاتر
    var acts = new Set(approved.map(function(u) { return u.activity; }));
    buildFilters(acts);
    doFilter('all', document.querySelector('.fbtn.active'));
}

// مساعدات صفوف الجدول
function row4(n, name, spec, act) {
    return '<tr><td class="num">' + n + '</td><td>' + name + '</td>' +
           '<td class="sp">' + (spec||'–') + '</td><td>' + act + '</td></tr>';
}
function row5(n, name, spec, act, action) {
    return '<tr><td class="num">' + n + '</td><td style="font-weight:700">' + name + '</td>' +
           '<td class="sp">' + (spec||'–') + '</td><td>' + act + 'NonNullList<' + action + '></td>' +
           '<tr>';
}

function badge(u) {
    return u.category === 'A'
        ? '<span class="bs">' + u.activity + '</span>'
        : '<span class="bc">' + u.activity + '</span>';
}

function typeLbl(u) {
    return u.category === 'A'
        ? '<span class="ts">🏃 رياضي</span>'
        : '<span class="tc">🎭 ثقافي</span>';
}

// ===== فلاتر =====
function buildFilters(acts) {
    var container = document.getElementById('filterBtns');
    if (!container) return;
    var allBtn = container.querySelector('.fbtn') || document.createElement('button');
    allBtn.className   = 'fbtn active';
    allBtn.textContent = 'الكل';
    allBtn.setAttribute('onclick', "doFilter('all',this)");
    container.innerHTML = '';
    container.appendChild(allBtn);
    acts.forEach(function(act) {
        var b = document.createElement('button');
        b.className   = 'fbtn';
        b.textContent = act;
        b.setAttribute('onclick', "doFilter('" + act.replace(/'/g,"\\'") + "',this)");
        container.appendChild(b);
    });
}

function doFilter(act, btn) {
    document.querySelectorAll('.fbtn').forEach(function(b) { b.classList.remove('active'); });
    if (btn) btn.classList.add('active');

    var titleEl = document.getElementById('filterTitle');
    if (titleEl)
        titleEl.textContent = act === 'all' ? 'جميع الطلبة المقبولين' : 'طلبة نشاط: ' + act;

    var approved = allStudents.filter(function(u) { return u.status === 'approved'; });
    var list = act === 'all' ? approved : approved.filter(function(u) { return u.activity === act; });

    var tbody   = document.getElementById('homeTbody');
    var emptyEl = document.getElementById('homeEmpty');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (list.length === 0) { if (emptyEl) emptyEl.style.display = 'flex'; return; }
    if (emptyEl) emptyEl.style.display = 'none';

    list.forEach(function(u, i) {
        tbody.innerHTML += '<tr>' +
            '<td class="num">' + (i+1) + '</td>' +
            '<td class="nm" onclick="openCard(' + u.id + ')">' + u.name + '</td>' +
            '<td class="sp">' + (u.specialty||'–') + '</td>' +
            '<td>' + badge(u) + '</td>' +
            '<td>' + typeLbl(u) + '</td>' +
            '</tr>';
    });
}

// ===== قبول / رفض =====
function approveUser(id) {
    if (!CAN_EDIT) { alert('غير مصرح لك'); return; }
    fetch('/api/students/' + id + '/status/', {
        method:  'POST',
        headers: { 'Content-Type':'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body:    JSON.stringify({ status: 'approved' }),
    }).then(function(r) { return r.json(); })
      .then(function(d) { if (d.success) loadData(); else alert('خطأ: ' + d.error); });
}

function rejectUser(id) {
    if (!CAN_EDIT) { alert('غير مصرح لك'); return; }
    if (!confirm('هل تريد رفض هذا الطلب وحذفه نهائياً؟')) return;
    fetch('/api/students/' + id + '/delete/', {
        method:  'DELETE',
        headers: { 'X-CSRFToken': CSRF_TOKEN },
    }).then(function(r) { return r.json(); })
      .then(function(d) { if (d.success) loadData(); else alert('خطأ: ' + d.error); });
}

// ===== عرض الجدول الزمني =====
function openSched(id) {
    var user = allStudents.find(function(u) { return u.id === id; });
    if (!user || !user.schedule) { alert('لا يوجد جدول زمني مرفق.'); return; }

    setText('schedModalTitle', 'الجدول الزمني – ' + user.name);
    var body = document.getElementById('schedModalBody');
    body.innerHTML = '';

    if (/\.(jpg|jpeg|png|gif|webp)$/i.test(user.schedule)) {
        var img = document.createElement('img');
        img.src = user.schedule;
        img.style.cssText = 'max-width:100%;border-radius:9px;display:block;margin:0 auto;';
        body.appendChild(img);
    } else if (/\.pdf$/i.test(user.schedule)) {
        var em = document.createElement('embed');
        em.src  = user.schedule;
        em.type = 'application/pdf';
        em.style.cssText = 'width:100%;height:520px;border-radius:9px;border:none;';
        body.appendChild(em);
    } else {
        body.innerHTML = '<p style="text-align:center;color:#888;padding:30px;">لا يمكن عرض هذا الملف مباشرة.</p>';
    }
    document.getElementById('schedModal').style.display = 'flex';
}

function closeSchedModal(e) {
    var m = document.getElementById('schedModal');
    if (!m) return;
    if (!e || e.target === m) m.style.display = 'none';
}

// ===== عرض البطاقة =====
// ===== عرض البطاقة =====
// ===== عرض البطاقة =====
// ===== عرض البطاقة =====
function openCard(id) {
    var u = allStudents.find(function(s) { return s.id === id; });
    if (!u) return;

    var isA = u.category === 'A';

    // العنوان
    var titleEl = document.getElementById('cardMainTitle');
    if (titleEl) titleEl.textContent = isA ? 'بطاقة الطالب الرياضي' : 'بطاقة الطالب الثقافي';

    // الشارة
    var badgeEl = document.getElementById('cardActivityBadge');
    if (badgeEl) {
        badgeEl.textContent      = isA ? 'رياضي' : 'ثقافي';
        badgeEl.style.background = isA ? '#2e7d32' : '#6a1b9a';
    }

    // تسمية النشاط
    var actLbl = document.getElementById('cardActivityLabel');
    if (actLbl) actLbl.textContent = isA ? 'نوع الرياضة' : 'النشاط الثقافي';

    // الأسماء
    var fn = function(elId, val) {
        var el = document.getElementById(elId);
        if (el) el.textContent = val || '—';
    };

    fn('cardLastNameAr',  u.last_name_ar);
    fn('cardFirstNameAr', u.first_name_ar);
    fn('cardLastNameFr',  u.last_name_fr);
    fn('cardFirstNameFr', u.first_name_fr);
    fn('cardBirthDate',   u.birth_date);
    fn('cardBirthPlace',  u.birth_place || '—');  // ← التعديل هنا
    fn('cardCategory',    isA ? 'رياضي' : 'ثقافي');
    fn('cardActivityType', u.activity);
    fn('cardRegNum',      u.matricule);
    fn('cardRegNum2',     u.matricule);

    // السنة الدراسية
    var yearEl = document.querySelector('.acad-year');
    if (yearEl) yearEl.textContent = u.academic_year || '2025 / 2026';

    // الصورة
    var photoEl = document.getElementById('cardPhoto');
    if (photoEl) {
        if (u.photo) {
            photoEl.src           = u.photo;
            photoEl.style.display = 'block';
        } else {
            photoEl.src           = '';
            photoEl.style.display = 'none';
        }
    }

    // إظهار البطاقة
    document.getElementById('cardModal').style.display = 'flex';
}
function setField(id, text, src) {
    var el = document.getElementById(id);
    if (!el) return;
    if (src !== undefined) el.src = src;
    else el.textContent = text;
}

function closeCardModal(e) {
    var m = document.getElementById('cardModal');
    if (!m) return;
    if (!e || e.target === m) m.style.display = 'none';
}

// ===== تشغيل =====
loadData();