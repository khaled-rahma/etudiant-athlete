// static/js/dashboard-config.js
// هذا الملف يستقبل المتغيرات من Django

var CSRF_TOKEN = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
var USER_ROLE = document.getElementById('user-role')?.textContent || '';
var CAN_EDIT = document.getElementById('can-edit')?.textContent === 'true';