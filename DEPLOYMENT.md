# دليل النشر على Heroku

## خطوات النشر السريع

### 1. إعداد Heroku CLI
تأكد من تثبيت Heroku CLI على جهازك:
```bash
# تحميل Heroku CLI من الموقع الرسمي
# https://devcenter.heroku.com/articles/heroku-cli

# تسجيل الدخول
heroku login
```

### 2. إنشاء التطبيق
```bash
# إنشاء تطبيق جديد
heroku create your-app-name

# إضافة قاعدة البيانات
heroku addons:create heroku-postgresql:essential-0

# إضافة buildpack لـ FFmpeg
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add --index 2 heroku/python
```

### 3. تعيين المتغيرات البيئية
```bash
# مفتاح الجلسة السري
heroku config:set SESSION_SECRET=$(openssl rand -base64 32)

# بيئة الإنتاج
heroku config:set FLASK_ENV=production

# عرض المتغيرات المعينة
heroku config
```

### 4. رفع الكود
```bash
# إضافة remote repository
heroku git:remote -a your-app-name

# رفع الكود
git add .
git commit -m "Initial deployment to Heroku"
git push heroku main
```

### 5. تشغيل قاعدة البيانات
```bash
# تشغيل إعداد قاعدة البيانات
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"

# عرض logs للتأكد من التشغيل
heroku logs --tail
```

## النشر التلقائي مع GitHub

### إعداد GitHub Actions

1. **إضافة Secrets في GitHub Repository:**
   - `HEROKU_API_KEY`: مفتاح API من Heroku
   - `HEROKU_APP_NAME`: اسم التطبيق
   - `HEROKU_EMAIL`: بريدك الإلكتروني في Heroku

2. **الحصول على مفتاح API:**
```bash
heroku auth:token
```

3. **ربط Repository:**
   - اذهب إلى Settings > Secrets and variables > Actions
   - أضف المتغيرات المطلوبة

## إعدادات الإنتاج

### تحسين الأداء
```bash
# تعيين عدد العمليات
heroku ps:scale web=1

# تعيين حجم الخادم (اختياري)
heroku ps:resize web=basic
```

### مراقبة التطبيق
```bash
# عرض الحالة
heroku ps

# عرض logs المباشرة
heroku logs --tail

# إعادة تشغيل
heroku restart
```

### إدارة قاعدة البيانات
```bash
# الاتصال بقاعدة البيانات
heroku pg:psql

# إنشاء نسخة احتياطية
heroku pg:backups:capture

# عرض معلومات قاعدة البيانات
heroku pg:info
```

## استكشاف الأخطاء

### مشاكل شائعة

1. **خطأ في buildpack:**
```bash
heroku buildpacks:clear
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add heroku/python
```

2. **مشاكل في قاعدة البيانات:**
```bash
heroku pg:reset DATABASE_URL
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

3. **مشاكل في المتغيرات:**
```bash
heroku config:unset VARIABLE_NAME
heroku config:set VARIABLE_NAME=new_value
```

## تحديث التطبيق

```bash
# سحب آخر التحديثات
git pull origin main

# رفع التحديثات
git push heroku main

# إعادة تشغيل إذا لزم الأمر
heroku restart
```

## مراقبة الأداء

### Heroku Metrics (مجاني)
- Response time
- Throughput
- Memory usage
- Error rate

### Commands مفيدة
```bash
# عرض استهلاك الذاكرة
heroku logs --source app --dyno web

# عرض إحصائيات الأداء
heroku ps:exec
top

# تحليل logs
heroku logs --num 500 | grep ERROR
```

## النسخ الاحتياطية

### قاعدة البيانات
```bash
# إنشاء نسخة احتياطية
heroku pg:backups:capture --app your-app-name

# جدولة نسخ احتياطية يومية
heroku pg:backups:schedule DATABASE_URL --at "02:00 UTC" --app your-app-name

# تحميل نسخة احتياطية
heroku pg:backups:download
```

### الكود
- تأكد من رفع جميع التغييرات إلى GitHub
- استخدم GitHub Releases للإصدارات المهمة

## الدومين المخصص (اختياري)

```bash
# إضافة دومين مخصص
heroku domains:add www.your-domain.com

# عرض DNS targets
heroku domains

# إعداد SSL (تلقائي في Heroku)
heroku certs:auto:enable
```

---

**ملاحظة:** تأكد من قراءة شروط استخدام Heroku وحدود الخطة المجانية قبل النشر.