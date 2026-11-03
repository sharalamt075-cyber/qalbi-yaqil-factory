from flask import Flask, request, redirect, session, render_template_string
import os

app = Flask(__name__)
app.secret_key = "qalbi-yaqil-secret-2024"
PASSWORD = "ZIZO"

LOGIN_HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>دخول خاص</title>
<style>
body{background:#0f0f0f;color:white;text-align:center;padding:40px;font-family:sans-serif}
.card{background:#1e1e1e;padding:30px;border-radius:20px;max-width:400px;margin:auto}
input{padding:15px;width:80%;border-radius:10px;border:none;margin:15px 0;font-size:18px;text-align:center}
button{background:#ff4081;color:white;padding:15px 30px;border:none;border-radius:10px;font-size:18px;cursor:pointer;width:85%}
.err{color:#ff5252}
</style>
</head>
<body>
<div class="card">
<h2>🔒 مصنع قلبي يقيل</h2>
<p>للاستخدام الشخصي فقط</p>
<form method="POST">
<input type="password" name="password" placeholder="كلمة السر">
<br>
<button>دخول</button>
</form>
{% if error %}<p class="err">{{ error }}</p>{% endif %}
</div>
</body>
</html>
"""

FACTORY_HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مصنع قلبي يقيل - خاص</title>
<style>
body{background:#0f0f0f;color:white;text-align:center;padding:30px;font-family:sans-serif}
.card{background:#1e1e1e;padding:25px;border-radius:20px;max-width:600px;margin:auto}
h1{color:#ff4081} .green{color:#00e676} .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px;text-align:right}
.agent{background:#2a2a2a;padding:10px;border-radius:10px;font-size:13px}
.agent span{color:#00e676}
.btn{background:#333;color:white;padding:10px 20px;border-radius:10px;text-decoration:none;display:inline-block;margin-top:20px}
</style>
</head>
<body>
<div class="card">
<h1>💖 قلبي يقيل - مصنعك الخاص</h1>
<p class="green">● Live 24/7 - هاتفك يمكن أن يكون مطفأ</p>
<p>أهلاً بك يا صاحب المصنع</p>
<p>المدير يدير 21 موظف الآن</p>
<div class="grid">
<div class="agent"><span>●</span> 01 راصد - يصطاد الترند</div>
<div class="agent"><span>●</span> 02 حكيم - يبحث الدراسة</div>
<div class="agent"><span>●</span> 03 خطاف - يكتب الهوك</div>
<div class="agent"><span>●</span> 04 لسان - يكتب بلهجتك</div>
<div class="agent"><span>●</span> 05 مدقق - يدقق النص</div>
<div class="agent"><span>●</span> 06 ميقاتي - توقيت الكلمات</div>
<div class="agent"><span>●</span> 07 صافي - ينظف الصوت</div>
<div class="agent"><span>●</span> 08 ذهبي - قلب ذهبي</div>
<div class="agent"><span>●</span> 09 أحمر - رقم 1 نابض</div>
<div class="agent"><span>●</span> 10 حركي - يحرك الكلمات</div>
<div class="agent"><span>●</span> 11 لحني - موسيقى</div>
<div class="agent"><span>●</span> 12 جامع - مونتاج نهائي</div>
<div class="agent"><span>●</span> 21 طبيب - مستشفى يحرس</div>
</div>
<p style="margin-top:20px">🎙️ ارفع صوت 42 ثانية ليبدأ المصنع</p>
<a class="btn" href="/logout">خروج آمن</a>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def login():
    if session.get('logged'):
        return render_template_string(FACTORY_HTML)
    error = None
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged'] = True
            return redirect('/')
        else:
            error = "كلمة السر خطأ"
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
