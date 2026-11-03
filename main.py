from flask import Flask, request, session, redirect, send_file, jsonify
import os, json, random, datetime, math
from PIL import Image, ImageDraw
app = Flask(__name__)
app.secret_key = "zizo-v3-light"

MEM_FILE = "/tmp/mem.json"
VIDEO_FILE = "/tmp/qalbi.mp4"
AUDIO_FILE = "/tmp/in.mp3"

def load_mem():
    try:
        if os.path.exists(MEM_FILE):
            with open(MEM_FILE,'r') as f: return json.load(f)
    except: pass
    agents={}
    names=["راصد","حكيم","خطاف","لسان نيون","هندسة","جزيئات","موجة","ذهبي","أحمر","حركي","لحني","جامع","ملون","قصاص","ناقد","مسرع","مبطئ","مترجم","ناشر","حارس","طبيب"]
    for i,n in enumerate(names,1):
        agents[f"a{i}"]={"name":n,"level":1,"xp":random.randint(10,28),"jobs":1}
    return {"total":1,"factory_level":1,"agents":agents,"log":["مصنع V3 الخفيف جاهز"]}

def save_mem(m):
    try:
        with open(MEM_FILE,'w') as f: json.dump(m,f)
    except: pass

HTML="""
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مصنع V3</title>
<style>
body{background:#060606;color:#fff;font-family:sans-serif;padding:12px;margin:0}
.card{background:#131313;padding:16px;border-radius:20px;max-width:800px;margin:auto;border:1px solid #333}
h1{color:#ffca28;text-align:center}
.upload{background:linear-gradient(135deg,#ffca28,#ff4081);padding:16px;border-radius:14px;text-align:center;font-weight:bold;cursor:pointer;display:block;margin:14px 0}
.upload input{display:none}
.status{background:#111;padding:12px;border-radius:10px;text-align:center;border:1px dashed #444;margin:10px 0}
#videoBox{display:block;background:#000;padding:14px;border-radius:14px;margin-top:14px;border:2px solid #00e676;text-align:center}
.download{background:linear-gradient(135deg,#00e676,#00bfa5);color:#000;padding:14px;border-radius:12px;display:block;text-align:center;text-decoration:none;font-weight:bold;margin-top:10px}
</style></head>
<body>
<div class="card">
<h1>💛 مصنع قلبي يقيل V3 - خفيف وسريع 💛</h1>
<div id="status" class="status">✅ المصنع جاهز - ارفع صوتك لصنع فيديو احترافي</div>
<label class="upload">📤 اضغط هنا لرفع الصوت - فيديو احترافي 42 ثانية
<input type="file" id="file" accept="audio/*" onchange="upload()"></label>
<div id="videoBox">
<h3 style="color:#00e676">🎬 معاينة الفيديو الاحترافي</h3>
<video id="preview" controls style="width:100%;border-radius:12px;background:#111" playsinline src="/download"></video>
<a href="/download" class="download">⬇️ تنزيل الفيديو MP4 - اضغط هنا</a>
<p style="font-size:11px;color:#999">إذا لم يعمل الفيديو، ارفع صوت جديد أولاً</p>
</div>
</div>
<script>
async function upload(){
 let file=document.getElementById('file').files[0];if(!file)return;
 let s=document.getElementById('status');s.innerText='⏳ يصنع فيديو احترافي... 20 ثانية';
 let fd=new FormData();fd.append('audio',file);
 let res=await fetch('/api/make',{method:'POST',body:fd});
 let data=await res.json();
 s.innerText='✅ اكتمل! انزل لتحت وشغل الفيديو وحمله';
 document.getElementById('preview').src='/download?t='+Date.now();
}
</script>
</body></html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    mem=load_mem()
    if session.get("logged"): return HTML
    if request.method=="POST":
        if request.form.get("password","").strip().upper()=="ZIZO":
            session["logged"]=True
            return redirect("/")
    return '<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:#050505;color:#fff;text-align:center;padding:40px"><div style="background:#151515;padding:26px;border-radius:20px;max-width:360px;margin:auto"><h2>🔒 مصنع V3</h2><form method="POST"><input type="password" name="password" placeholder="ZIZO" style="padding:14px;width:80%;border-radius:10px;border:none;text-align:center;margin:12px"><br><button style="background:#ffca28;color:#000;padding:14px 28px;border:none;border-radius:10px;width:85%;font-weight:bold">دخول</button></form></div></body></html>'

@app.route("/api/mem")
def api_mem(): return jsonify(load_mem())

@app.route("/api/make", methods=["POST"])
def make():
    mem=load_mem()
    f=request.files.get('audio')
    if f: f.save(AUDIO_FILE)
    mem["total"]+=1
    save_mem(mem)
    try:
        from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
        from PIL import Image, ImageDraw
        import numpy as np
        
        audio=AudioFileClip(AUDIO_FILE)
        dur=min(audio.duration, 42)
        
        # خلفية سوداء
        base=ColorClip((1080,1920), color=(0,0,0), duration=dur)
        
        # صورة القلب الذهبي
        img=Image.new('RGB', (1080,1920), (0,0,0))
        draw=ImageDraw.Draw(img, 'RGBA')
        cx,cy=540,800
        # هندسة إسلامية
        for r in [300,550,750]:
            pts=[]
            for i in range(16):
                ang=i*360/16
                x=cx+r*math.cos(math.radians(ang))
                y=cy+r*math.sin(math.radians(ang))
                pts.append((x,y))
            draw.line(pts+[pts[0]], fill=(255,215,0,25), width=1)
        # قلب ذهبي نيون
        for g in [40,25,12]:
            draw.ellipse((cx-200-g, cy-200-g, cx+200+g, cy+200+g), outline=(255,215,0,g), width=2)
        draw.text((cx, cy), "قلبك", fill=(255,220,0), anchor="mm")
        draw.text((cx, cy+90), "يفكر قبل عقلك", fill=(255,255,255), anchor="mm")
        draw.text((cx, 100), "قلبي يقيل ♡", fill=(255,215,0), anchor="mm")
        draw.text((cx, 1800-250), "40,000 خلية - هارفارد 2024", fill=(255,215,0), anchor="mm")
        img.save("/tmp/bg.png")
        
        bg_clip=ImageClip("/tmp/bg.png", duration=dur)
        final=CompositeVideoClip([base, bg_clip]).set_audio(audio.subclip(0,dur))
        final.write_videofile(VIDEO_FILE, fps=24, codec='libx264', audio_codec='aac', verbose=False, logger=None)
    except Exception as e:
        print("video error", e)
    return jsonify({"ok":True,"mem":mem})

@app.route("/download")
def dl():
    if os.path.exists(VIDEO_FILE):
        return send_file(VIDEO_FILE, as_attachment=False, mimetype="video/mp4")
    # لو لا يوجد فيديو، أرسل الصوت الأصلي
    if os.path.exists(AUDIO_FILE):
        return send_file(AUDIO_FILE, as_attachment=False, mimetype="audio/mpeg")
    return "ارفع صوت أولا", 404

@app.route("/logout")
def logout(): session.clear(); return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
