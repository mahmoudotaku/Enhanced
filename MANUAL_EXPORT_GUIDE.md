# دليل التصدير اليدوي للمشروع

## الطريقة الأولى: تحميل الملفات وتصديرها

### 1. تحميل المشروع من Replit
- في أعلى يسار الشاشة، اضغط على النقاط الثلاث (⋮)
- اختر "Download as zip"
- احفظ الملف على جهازك واستخرجه

### 2. إنشاء Repository على GitHub
- اذهب إلى [github.com](https://github.com)
- اضغط "New repository"
- اسم المشروع: `arabic-video-downloader`
- اختر Public
- ضع ✓ على "Add a README file"
- اضغط "Create repository"

### 3. رفع الملفات
- في صفحة Repository الجديد
- اضغط "uploading an existing file"
- اسحب جميع ملفات المشروع (ما عدا README.md الفارغ)
- اكتب رسالة: "Arabic Video Downloader - Complete Project"
- اضغط "Commit changes"

## الطريقة الثانية: استخدام GitHub Desktop

### 1. تحميل GitHub Desktop
- حمل GitHub Desktop من [desktop.github.com](https://desktop.github.com)
- سجل الدخول بحساب GitHub

### 2. إنشاء Repository محلي
- في GitHub Desktop: File → New Repository
- اسم: `arabic-video-downloader`
- مكان الحفظ: اختر مجلد فارغ
- اضغط "Create Repository"

### 3. نسخ ملفات المشروع
- انسخ جميع ملفات المشروع من Replit إلى المجلد الجديد
- في GitHub Desktop ستظهر التغييرات
- اكتب وصف: "Complete Arabic Video Downloader"
- اضغط "Commit to main"
- اضغط "Publish repository"

## الطريقة الثالثة: استخدام Git في Terminal المحلي

### إذا كان لديك Git على جهازك:

```bash
# إنشاء مجلد جديد
mkdir arabic-video-downloader
cd arabic-video-downloader

# تهيئة Git
git init

# نسخ الملفات من Replit هنا

# إضافة الملفات
git add .
git commit -m "Initial commit: Arabic Video Downloader"

# ربط بـ GitHub (غير YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/arabic-video-downloader.git
git branch -M main
git push -u origin main
```

## الملفات المهمة للتصدير

تأكد من وجود هذه الملفات:

### ملفات التطبيق الأساسية:
- ✅ main.py
- ✅ app.py  
- ✅ models.py
- ✅ routes.py
- ✅ utils.py

### ملفات الواجهة:
- ✅ templates/ (مجلد كامل)
- ✅ static/ (مجلد كامل)

### ملفات التكوين:
- ✅ pyproject.toml
- ✅ uv.lock
- ✅ runtime.txt
- ✅ Procfile
- ✅ app.json
- ✅ heroku.yml

### ملفات Git:
- ✅ .gitignore
- ✅ .env.example
- ✅ .github/workflows/deploy.yml

### ملفات التوثيق:
- ✅ README.md
- ✅ DEPLOYMENT.md
- ✅ GIT_SETUP.md
- ✅ LICENSE

## بعد التصدير: النشر على Heroku

```bash
# تسجيل الدخول
heroku login

# إنشاء تطبيق
heroku create arabic-video-downloader-app

# إضافة قاعدة البيانات
heroku addons:create heroku-postgresql:essential-0

# تعيين المتغيرات
heroku config:set SESSION_SECRET=your-secret-key-here

# النشر
git push heroku main

# تفعيل قاعدة البيانات
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

أي طريقة تفضل؟