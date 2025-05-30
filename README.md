# موقع تحميل الفيديوهات المتطور

موقع ويب باللغة العربية لتحميل الفيديوهات من أكثر من 1000 منصة مختلفة بما في ذلك YouTube وTikTok وInstagram وFacebook وTwitter والكثير من المنصات الأخرى.

## المميزات الرئيسية

### 🎬 دعم شامل للمنصات
- **YouTube** - جميع أنواع الفيديوهات والقوائم
- **TikTok** - فيديوهات قصيرة وطويلة
- **Instagram** - منشورات، قصص، وريلز
- **Facebook** - فيديوهات عامة ومشاركة
- **Twitter/X** - فيديوهات وGIFs
- **أكثر من 995 موقع آخر** - بفضل مكتبة yt-dlp

### 💎 تصميم متطور
- **تصميم Glass Morphism** - مظهر عصري وجذاب
- **دعم كامل للغة العربية** - واجهة RTL مع خطوط عربية
- **ثيم فاتح وداكن** - قابلية تبديل سهلة
- **تصميم متجاوب** - يعمل على جميع الأجهزة

### ⚡ أداء متقدم
- **تتبع التقدم المباشر** - مراقبة حالة التحميل لحظياً
- **معالجة خلفية** - تحميل متعدد بدون تجميد الواجهة
- **تنظيف تلقائي** - حذف الملفات القديمة تلقائياً
- **ذاكرة التحميلات** - حفظ سجل كامل للتحميلات

### 🎯 خيارات متنوعة
- **جودات متعددة** - من 360p إلى 4K
- **تحميل الصوت فقط** - استخراج MP3
- **معاينة المحتوى** - عرض تفاصيل الفيديو قبل التحميل
- **تحميل سريع** - سرعة مُحسنة

## 🚀 النشر السريع على Heroku

### النشر بضغطة واحدة
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### النشر اليدوي

1. **إنشاء تطبيق Heroku**
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:essential-0
```

2. **تعيين متغيرات البيئة**
```bash
heroku config:set SESSION_SECRET=your-secret-key-here
heroku config:set FLASK_ENV=production
```

3. **رفع الكود ونشره**
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

## متطلبات النظام

### للتطوير المحلي
- Python 3.11+
- PostgreSQL (للإنتاج) أو SQLite (للتطوير)
- FFmpeg

### للنشر على Heroku
- حساب Heroku
- حساب GitHub
- PostgreSQL add-on

## التثبيت والإعداد المحلي

### 1. استنساخ المشروع
```bash
git clone https://github.com/yourusername/arabic-video-downloader.git
cd arabic-video-downloader
```

### 2. إعداد البيئة الافتراضية
```bash
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate
pip install -r pyproject.toml
```

### 3. إعداد قاعدة البيانات
```bash
# نسخ ملف المتغيرات
cp .env.example .env

# تحرير المتغيرات (اختياري للتطوير المحلي)
# DATABASE_URL=sqlite:///video_downloader.db
# SESSION_SECRET=your-secret-key
```

### 4. تشغيل التطبيق
```bash
python main.py
```

## 📁 هيكل المشروع

```
arabic-video-downloader/
├── app.py                 # إعداد Flask والقاعدة
├── main.py               # نقطة الدخول الرئيسية
├── models.py             # نماذج قاعدة البيانات
├── routes.py             # مسارات التطبيق وAPI
├── utils.py              # دوال مساعدة
├── Procfile              # إعداد Heroku
├── app.json              # وصف التطبيق لHeroku
├── runtime.txt           # إصدار Python
├── .env.example          # مثال للمتغيرات البيئية
├── static/
│   ├── css/
│   │   └── style.css     # أنماط CSS مخصصة
│   └── js/
│       ├── main.js       # JavaScript رئيسي
│       └── progress.js   # تتبع التقدم
├── templates/
│   ├── base.html         # القالب الأساسي
│   ├── index.html        # الصفحة الرئيسية
│   └── history.html      # صفحة السجل
└── downloads/            # مجلد التحميلات المؤقت
```

## 🎨 المكونات التقنية

### Backend
- **Flask** - إطار العمل الأساسي
- **SQLAlchemy** - ORM لقاعدة البيانات
- **PostgreSQL** - قاعدة البيانات للإنتاج
- **yt-dlp** - مكتبة تحميل الفيديوهات
- **Gunicorn** - خادم WSGI للإنتاج

### Frontend
- **Bootstrap 5** - إطار تصميم متجاوب
- **Font Awesome** - أيقونات
- **خطوط Cairo** - خطوط عربية
- **JavaScript ES6** - تفاعل ديناميكي
- **CSS Grid/Flexbox** - تخطيط متقدم

## 🔧 المتغيرات البيئية

| المتغير | الوصف | مطلوب |
|---------|--------|--------|
| `DATABASE_URL` | رابط قاعدة البيانات | نعم |
| `SESSION_SECRET` | مفتاح الجلسات السري | نعم |
| `FLASK_ENV` | بيئة التشغيل | لا |

## 📝 استخدام API

### الحصول على معلومات الفيديو
```bash
curl -X POST https://your-app.herokuapp.com/api/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### بدء تحميل
```bash
curl -X POST https://your-app.herokuapp.com/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID", "quality": "720p"}'
```

### تتبع التقدم
```bash
curl https://your-app.herokuapp.com/api/progress/DOWNLOAD_ID
```

## 🛠️ التطوير والمساهمة

### إضافة ميزات جديدة
1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/new-feature`)
3. تطبيق التغييرات
4. اختبار شامل
5. إرسال Pull Request

### التحسينات المقترحة
- [ ] دعم التحميل المجمع
- [ ] إضافة قوائم التشغيل
- [ ] تحسين الأداء
- [ ] دعم المزيد من المنصات
- [ ] واجهة إدارة متقدمة

## 📜 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 🚨 تنبيهات مهمة

- تأكد من احترام حقوق النشر عند تحميل المحتوى
- استخدم الموقع للاستخدام الشخصي فقط
- لا تحمل محتوى محمي بحقوق الطبع والنشر بدون إذن

## 📞 الدعم

إذا واجهت أي مشاكل أو لديك اقتراحات:
- افتح issue في GitHub
- راسلنا عبر البريد الإلكتروني
- انضم لمجتمع المطورين

---

**صنع بـ ❤️ من أجل المجتمع العربي**
