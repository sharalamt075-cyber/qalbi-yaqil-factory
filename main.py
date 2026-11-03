from flask import Flask, request, session, redirect
import os
app = Flask(__name__)
app.secret_key = "zizo-secret-123"
@app.route("/", methods=["GET", "POST"])
def home():
    if session.get("logged"):
        return '<html dir="rtl"><body style="background:#0f0f0f;color:white;text-align:center;padding:50px;font-family:sans-serif"><div style="background:#1e1e1e;padding:30px;border-radius:20px;max-width:400px;margin:auto"><h1 style="color:#ff4081">💖 قلبي يقيل</h1><p style="color:#00e676">● Live 24/7</p><p>دخلت بنجاح بكلمة ZIZO</p><p>مصنعك الخاص جاهز</p><a href="/logout" style="color:#aaa">خروج</a></div></body></html>'
    err=""
    if request.method=="POST":
        if request.form.get("password","").strip().upper()=="ZIZO":
            session["logged"]=True
            return redirect("/")
        else:
            err="كلمة السر خطأ - اكتب ZIZO حروف كبيرة"
    return f'<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="background:#0f0f0f;color:white;text-align:center;padding:50px;font-family:sans-serif"><div style="background:#1e1e1e;padding:30px;border-radius:20px;max-width:350px;margin:auto"><h2>🔒 مصنعك الخاص</h2><p>للاستخدام الشخصي فقط</p><form method="POST"><input type="password" name="password" placeholder="اكتب ZIZO" style="padding:15px;width:80%;border-radius:10px;border:none;margin:15px;font-size:18px;text-align:center"><br><button style="background:#ff4081;color:white;padding:15px 30px;border:none;border-radius:10px;font-size:18px;width:85%">دخول</button></form><p style="color:#ff5252">{err}</p></div></body></html>'
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
