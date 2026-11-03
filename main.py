from flask import Flask, request, redirect, session, render_template_string
import os
app = Flask(__name__)
app.secret_key = "qalbi-secret"
PASSWORD = "ZIZO"

LOGIN = """
<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content=width=device-width,initial-scale=1>
<style>body{background:#0f0f0f;color:#fff;text-align:center;padding:50px;font-family:sans-serif}
.card{background:#1e1e1e;padding:30px;border-radius:20px;max-width:350px;margin:auto}
input{padding:15px;width:80%;border-radius:10px;border:none;margin:15px;font-size:18px;text-align:center}
button{background:#ff4081;color:#fff;padding:15px 30px;border:none;border-radius:10px;font-size:18px;width:85%}</style>
</head><body><div class=card><h2>🔒 مصنعك الخاص</h2><p>اكتب كلمة السر</p>
<form method=POST><input type=password name=password placeholder=ZIZO><br><button>دخول</button></form>
<p>{msg}</p></div></body></html>
"""

FACTORY = """
<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content=width=device-width,initial-scale=1>
<style>body{background:#0f0f0f;color:#fff;text-align:center;padding:40px;font-family:sans-serif}
.card{background:#1e1e1e;padding:30px;border-radius:20px;max-width:500px;margin:auto}
h1{color:#ff4081}.green{color:#00e676}</style>
</head><body><div class=card><h1>💖 قلبي يقيل</h1><p class=green>● Live 24/7</p>
<p>دخلت بنجاح! هذا مصنعك الخاص</p><p>21 موظف يعملون الآن</p></div></body></html>
"""

@app.route('/', methods=['GET','POST'])
def home():
    if session.get('ok'): return FACTORY
    msg=""
    if request.method=='POST':
        if request.form.get('password','').strip().upper()=="ZIZO":
            session['ok']=True
            return redirect('/')
        else: msg="كلمة السر خطأ"
    return LOGIN.replace("{msg}",msg)

@app.route('/health')
def health(): return "OK"

if __name__=='__main__':
    port=int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0',port=port)
