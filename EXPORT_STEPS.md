# خطوات تصدير المشروع إلى GitHub

## الأوامر المطلوبة

بعد إنشاء Repository على GitHub والحصول على Personal Access Token، شغل هذه الأوامر في Terminal:

### 1. إعداد Git
```bash
# تعيين معلومات Git (غير البيانات بمعلوماتك)
git config --global user.name "اسمك"
git config --global user.email "بريدك@gmail.com"
```

### 2. ربط المشروع بـ GitHub
```bash
# إزالة الريموت الحالي إن وجد
git remote remove origin

# إضافة GitHub repository (غير YOUR_USERNAME باسم حسابك)
git remote add origin https://github.com/YOUR_USERNAME/arabic-video-downloader.git

# التحقق من الريموت
git remote -v
```

### 3. إضافة الملفات والرفع
```bash
# إضافة جميع الملفات
git add .

# عمل commit
git commit -m "Initial commit: Arabic Video Downloader - Complete Project"

# تعيين الفرع الرئيسي
git branch -M main

# رفع الكود (ستحتاج لإدخال username والtoken)
git push -u origin main
```

### 4. بيانات الدخول
عند السؤال عن:
- **Username:** اسم حسابك على GitHub
- **Password:** Personal Access Token الذي حصلت عليه (ليس كلمة المرور العادية)

## بديل: استخدام Git مع Token في الرابط
```bash
# يمكنك استخدام هذا الأمر مباشرة (غير البيانات)
git remote add origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/arabic-video-downloader.git
git push -u origin main
```

## التحقق من النجاح
بعد الانتهاء، ستجد المشروع في حسابك على GitHub مع جميع الملفات:
- الكود الكامل
- ملفات التوثيق
- إعدادات النشر على Heroku
- GitHub Actions للنشر التلقائي