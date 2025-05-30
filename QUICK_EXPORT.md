# تصدير سريع للمشروع إلى GitHub

## خطوات التصدير السريعة

### 1. إنشاء Repository على GitHub
- اذهب إلى GitHub.com
- اضغط "New Repository"
- سمي المشروع: `arabic-video-downloader`
- اختر Public أو Private
- لا تضع ✓ على Initialize with README (لأننا لدينا ملفات بالفعل)

### 2. تصدير الملفات
بعد إنشاء Repository، انسخ هذه الأوامر وشغلها:

```bash
git remote remove origin
git remote add origin https://github.com/اسم-المستخدم/arabic-video-downloader.git
git add .
git commit -m "Arabic Video Downloader - Complete Project"
git branch -M main
git push -u origin main
```

### 3. إعداد النشر التلقائي على Heroku
في GitHub Repository:
1. اذهب إلى Settings → Secrets and variables → Actions
2. أضف هذه المتغيرات:
   - `HEROKU_API_KEY`: احصل عليه من Heroku Dashboard → Account Settings
   - `HEROKU_APP_NAME`: اسم التطبيق الذي ستنشئه على Heroku
   - `HEROKU_EMAIL`: بريدك الإلكتروني في Heroku

### 4. النشر على Heroku
```bash
heroku create arabic-video-downloader-app
heroku addons:create heroku-postgresql:essential-0
heroku config:set SESSION_SECRET=your-secret-key-here
git push heroku main
```

## الملفات المُعدة للتصدير ✓

- ✓ README.md - توثيق شامل بالعربية
- ✓ .gitignore - ملف تجاهل Git
- ✓ .env.example - مثال للمتغيرات البيئية
- ✓ .github/workflows/deploy.yml - نشر تلقائي
- ✓ Procfile - إعداد Heroku
- ✓ app.json - وصف التطبيق
- ✓ runtime.txt - إصدار Python
- ✓ pyproject.toml - المكتبات المطلوبة
- ✓ GIT_SETUP.md - دليل مفصل
- ✓ DEPLOYMENT.md - دليل النشر

## المشروع جاهز 100% للتصدير! 🚀