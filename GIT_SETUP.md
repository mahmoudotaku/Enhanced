# دليل تصدير المشروع إلى Git

## إعداد Git Repository جديد

### 1. إنشاء Repository على GitHub

1. اذهب إلى [GitHub](https://github.com) وسجل الدخول
2. اضغط على "New Repository"
3. اختر اسم للمشروع مثل `arabic-video-downloader`
4. اختر إعدادات Repository:
   - ✅ Public (أو Private حسب الحاجة)
   - ✅ Add README.md
   - ✅ Add .gitignore (Python)
   - ✅ Choose license (MIT مُوصى به)

### 2. ربط المشروع المحلي بـ GitHub

```bash
# تهيئة Git في مجلد المشروع
git init

# إضافة جميع الملفات
git add .

# أول commit
git commit -m "Initial commit: Arabic Video Downloader"

# ربط بـ GitHub Repository
git remote add origin https://github.com/username/arabic-video-downloader.git

# رفع الكود
git branch -M main
git push -u origin main
```

### 3. إعداد GitHub Actions للنشر التلقائي

#### إضافة Secrets في GitHub:

1. اذهب إلى Repository Settings
2. اضغط على "Secrets and variables" → "Actions"
3. أضف المتغيرات التالية:

| Secret Name | كيفية الحصول عليه |
|-------------|-------------------|
| `HEROKU_API_KEY` | Heroku Dashboard → Account Settings → API Key |
| `HEROKU_APP_NAME` | اسم التطبيق في Heroku |
| `HEROKU_EMAIL` | البريد الإلكتروني المسجل في Heroku |

#### الحصول على Heroku API Key:

```bash
# تسجيل الدخول إلى Heroku
heroku login

# الحصول على API Key
heroku auth:token
```

## النشر على Heroku من Git

### طريقة 1: النشر التلقائي (مُوصى به)

بعد إعداد GitHub Actions، كل push إلى main branch سيؤدي إلى نشر تلقائي.

### طريقة 2: النشر اليدوي

```bash
# إنشاء تطبيق Heroku جديد
heroku create arabic-video-downloader-app

# إضافة قاعدة بيانات PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# تعيين المتغيرات البيئية
heroku config:set SESSION_SECRET=your-super-secret-key-here
heroku config:set FLASK_ENV=production

# نشر الكود
git push heroku main

# تشغيل قاعدة البيانات
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### طريقة 3: النشر بضغطة واحدة

استخدم الزر في README.md للنشر المباشر:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## إدارة الإصدارات

### إنشاء إصدار جديد

```bash
# تحديث الكود
git add .
git commit -m "وصف التحديثات"

# إنشاء tag للإصدار
git tag -a v1.0.0 -m "الإصدار الأول"

# رفع التحديثات والتags
git push origin main
git push origin --tags
```

### فروع التطوير

```bash
# إنشاء فرع جديد للتطوير
git checkout -b feature/new-feature

# بعد انتهاء التطوير
git checkout main
git merge feature/new-feature
git push origin main
```

## إعدادات متقدمة

### تحديث .gitignore

تأكد من أن .gitignore يحتوي على:

```
# ملفات التحميل
downloads/
*.mp4
*.mp3
*.webm
*.m4a

# ملفات البيئة
.env
.env.local
.env.production

# ملفات قاعدة البيانات المحلية
*.db
*.sqlite
*.sqlite3

# ملفات Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
```

### إعداد Pre-commit Hooks

```bash
# تثبيت pre-commit
pip install pre-commit

# إنشاء ملف .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
EOF

# تفعيل pre-commit
pre-commit install
```

## استكشاف الأخطاء

### مشاكل شائعة في Git

1. **رفض الـ push:**
```bash
git pull origin main --rebase
git push origin main
```

2. **مشاكل في الـ merge:**
```bash
git status
# حل التعارضات يدوياً
git add .
git commit -m "Resolve merge conflicts"
```

3. **إعادة تعيين commit خاطئ:**
```bash
git reset --soft HEAD~1  # إلغاء آخر commit مع الحفاظ على التغييرات
git reset --hard HEAD~1  # إلغاء آخر commit والتغييرات
```

### مشاكل النشر على Heroku

1. **خطأ في buildpack:**
```bash
heroku buildpacks:set heroku/python
```

2. **مشاكل قاعدة البيانات:**
```bash
heroku pg:reset DATABASE_URL --confirm app-name
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

3. **مراجعة logs:**
```bash
heroku logs --tail
```

## نصائح مهمة

### للأمان:
- لا تضع أبداً مفاتيح API في الكود
- استخدم متغيرات البيئة دائماً
- راجع .gitignore قبل كل commit

### للتنظيم:
- اكتب رسائل commit واضحة
- استخدم فروع منفصلة للميزات الجديدة
- اعمل backup للقاعدة قبل التحديثات الكبيرة

### للأداء:
- راجع حجم الملفات قبل الرفع
- استخدم .gitignore لاستبعاد الملفات الكبيرة
- نظف الملفات المؤقتة بانتظام

## مثال كامل للتصدير

```bash
# خطوات سريعة للتصدير
cd /path/to/your/project

# تهيئة Git
git init
git add .
git commit -m "إعداد مشروع تحميل الفيديوهات العربي"

# ربط بـ GitHub
git remote add origin https://github.com/yourusername/arabic-video-downloader.git
git branch -M main
git push -u origin main

# نشر على Heroku
heroku create your-app-name
heroku addons:create heroku-postgresql:essential-0
heroku config:set SESSION_SECRET=your-secret-key
git push heroku main

# تفعيل قاعدة البيانات
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "تم تصدير المشروع بنجاح! 🎉"
```

---

**ملاحظة:** تأكد من أن جميع المفاتيح السرية محفوظة بأمان ولا تشاركها في أي مكان عام.