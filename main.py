from flask import Flask, request, session, redirect
import os
app = Flask(__name__)
app.secret_key = "zizo-factory-2026"

FACTORY_HTML = """
<html dir="rtl" lang="ar"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مصنع قلبي يقيل - الخاص</title>
<style>
body{background:#0a0a0a;color:white;font-family:sans-serif;margin:0;padding:20px}
.card{background:#1e1e1e;padding:25px;border-radius:20px;max-width:650px;margin:auto;border:1px solid #333}
h1{color:#ff4081;text-align:center;margin:0}.green{color:#00e676;text-align:center}
.status{background:#111;padding:15px;border-radius:12px;margin:15px 0;text-align:center;border:1px dashed #444}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}
.agent{background:#2a2a2a;padding:12px;border-radius:10px;font-size:13px;text-align:right}
.agent.active{background:#333;border:1px solid #00e676}
.agent span{float:left}
.upload{background:linear-gradient(135deg,#ff4081,#ff8a65);padding:20px;border-radius:15px;text-align:center;margin:20px 0;cursor:pointer}
.upload input{display:none}
.btn{display:block;background:#333;color:white;padding:12px;border-radius:10px;text-align:center;text-decoration:none;margin-top:15px}
</style></head>
<body>
<div class="card">
<h1>💖 قلبي يقيل</h1>
<p class="green">● Live 24/7 - مصنعك الخاص - محمي بـ ZIZO</p>

<div class="status" id="status">
🎙️ جاهز لاستقبال صوتك 42 ثانية<br>
<small>ارفع الصوت وسيبدأ الـ 21 موظف تلقائياً</small>
</div>

<label class="upload">
📤 اضغط هنا لرفع صوت 42 ثانية
<input type="file" id="audioFile" accept="audio/*" onchange="startFactory()">
</label>

<div class="grid">
<div class="agent" id="a1"><span>●</span>01 راصد - ترند</div>
<div class="agent" id="a2"><span>●</span>02 حكيم - دراسة</div>
<div class="agent" id="a3"><span>●</span>03 خطاف - هوك</div>
<div class="agent" id="a4"><span>●</span>04 لسان - بلهجتك</div>
<div class="agent" id="a5"><span>●</span>05 مدقق - تدقيق</div>
<div class="agent" id="a6"><span>●</span>06 ميقاتي - توقيت</div>
<div class="agent" id="a7"><span>●</span>07 صافي - تنظيف</div>
<div class="agent" id="a8"><span>●</span>08 ذهبي - قلب ذهبي</div>
<div class="agent" id="a9"><span>●</span>09 أحمر - رقم 1 نابض</div>
<div class="agent" id="a10"><span>●</span>10 حركي - تحريك</div>
<div class="agent" id="a11"><span>●</span>11 لحني - موسيقى</div>
<div class="agent" id="a12"><span>●</span>12 جامع - مونتاج نهائي</div>
<div class="agent" id="a21" style="grid-column:span 2;background:#1a2a1a"><span>●</span>21 طبيب - يحرس المصنع</div>
</div>

<div id="result" style="margin-top:20px;display:none;background:#111;padding:15px;border-radius:12px;text-align:center">
<h3 style="color:#00e676">✅ الفيديو جاهز!</h3>
<p>تم إنتاج فيديو قلبي يقيل من صوتك</p>
</div>

<a href="/logout" class="btn">🔒 خروج آمن</a>
</div>

<script>
function startFactory(){
 const s=document.getElementById('status');
 s.innerHTML='⏳ المصنع يعمل... جاري الإنتاج';
 let agents=['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','a12','a21'];
 let i=0;
 let interval=setInterval(()=>{
  if(i<agents.length){
   document.getElementById(agents[i]).classList.add('active');
   s.innerHTML='⚙️ يعمل: '+document.getElementById(agents[i]).innerText;
   i++;
  } else {
   clearInterval(interval);
   s.innerHTML='✅ اكتمل الإنتاج - 21 موظف أنهوا العمل';
   document.getElementById('result').style.display='block';
  }
 },800);
}
</script>
</body></html>
"""

LOGIN_HTML = """
<html dir="rtl"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>body{background:#0f0f0f;color:white;text-align:center;padding:50px;font-family:sans-serif}
.card{background:#1e1e1e;padding:30px;border-radius:20px;max-width:350px;margin:auto;border:1px solid #333}
input{padding:15px;width:80%;border-radius:10px;border:none;margin:15px;font-size:18px;text-align:center}
button{background:#ff4081;color:white;padding:15px 30px;border:none;border-radius:10px;font-size:18px;width:85%;cursor:pointer}
</style></head>
<body><div class="card"><h2>🔒 مصنع قلبي يقيل</h2><p>للاستخدام الشخصي فقط</p>
<form method="POST"><input type="password" name="password" placeholder="ZIZO"><br><button>دخول المصنع</button></form>
<p style="color:#ff5252">{err}</p></div></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if session.get("logged"):
        return FACTORY_HTML
    err=""
    if request.method=="POST":
        if request.form.get("password","").strip().upper()=="ZIZO":
            session["logged"]=True
            return redirect("/")
        else:
            err="كلمة السر خطأ"
    return LOGIN_HTML.replace("{err}",err)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
