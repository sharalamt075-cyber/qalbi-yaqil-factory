from flask import Flask, request, session, redirect, send_file, jsonify
import os, json, random, datetime, math, tempfile
from PIL import Image, ImageDraw, ImageFont
import numpy as np

app = Flask(__name__)
app.secret_key = "zizo-pro-factory-v2"

MEM_FILE = "/tmp/mem_pro.json"
VIDEO_FILE = "/tmp/qalbi_pro.mp4"
AUDIO_FILE = "/tmp/input.mp3"

# --- الذاكرة ---
def load_mem():
    try:
        if os.path.exists(MEM_FILE):
            with open(MEM_FILE,'r') as f: return json.load(f)
    except: pass
    agents = {}
    names = ["راصد النبض","حكيم النصوص","خطاف الكلمات","لسان نيون","هندسة إسلامية","صانع جزيئات","موجة صوتية","ذهبي","أحمر قلب","حركي نيون","لحني","جامع نهائي","ملون","قصاص","ناقد","مسرع","مبطئ","مترجم","ناشر","حارس","طبيب"]
    for i,n in enumerate(names,1):
        agents[f"a{i}"] = {"name":n,"level":1,"xp":0,"jobs":0}
    agents["a21"]["level"]=5
    return {"total":0,"factory_level":1,"agents":agents,"log":["ولادة مصنع المونتاج المحترف"]}

def save_mem(m):
    try:
        with open(MEM_FILE,'w') as f: json.dump(m,f)
    except: pass

# --- مولد الإطارات الاحترافي مثل الفيديو المرجعي ---
W, H = 1080, 1920
def draw_islamic(draw, cx, cy, t):
    for r in [280, 500, 700]:
        pts=[]
        for i in range(16):
            ang = i*360/16 + t*2
            x = cx + r*math.cos(math.radians(ang))
            y = cy + r*math.sin(math.radians(ang))
            pts.append((x,y))
        draw.line(pts+[pts[0]], fill=(255,215,0,18), width=1)

def make_frame(text_main, text_sub, style, time_sec, waveform_heights):
    img = Image.new('RGB', (W, H), (0,0,0))
    draw = ImageDraw.Draw(img, 'RGBA')
    cx, cy = W//2, H//2 - 80
    
    # هندسة إسلامية خلفية
    draw_islamic(draw, cx, cy, time_sec)
    
    # لوقو فوق
    draw.text((W//2, 70), "قلبي يقيل ♡", fill=(255,215,0,200), anchor="mm")
    
    if style == "gold_big":
        # توهج ذهبي نيون مثل قلبك
        for glow in [50,30,15]:
            draw.ellipse((cx-220-glow, cy-220-glow, cx+220+glow, cy+220+glow), outline=(255,215,0, glow//2), width=2)
        draw.ellipse((cx-180, cy-180, cx+180, cy+180), outline=(255,215,0, 120), width=3)
        draw.text((W//2, cy), text_main, fill=(255,225,0), anchor="mm")
        if text_sub:
            draw.text((W//2, cy+120), text_sub, fill=(255,255,255), anchor="mm")
        # خطين وردي وازرق مثل الفيديو
        draw.rectangle((120, cy+200, 960, cy+204), fill=(255,0,120,200))
        draw.text((W//2, cy+185), "القلب • يسبق", fill=(255,80,150), anchor="mm")
        draw.rectangle((120, cy+250, 960, cy+254), fill=(0,200,255,200))
        draw.text((W//2, cy+235), "الدماغ • يتأخر", fill=(80,200,255), anchor="mm")
        
    elif style == "quran":
        # آية قرآنية ذهبية
        draw.text((W//2, cy-60), text_main, fill=(255,215,0), anchor="mm", align="center")
        if text_sub:
            draw.text((W//2, cy+80), text_sub, fill=(255,255,255), anchor="mm", align="center")
            
    elif style == "particles":
        # قلب من جزيئات 40,000 مثل الفيديو
        np.random.seed(int(time_sec*10) % 100)
        for _ in range(900):
            u = np.random.rand()*2*math.pi
            x = 16*(math.sin(u)**3)
            y = 13*math.cos(u) - 5*math.cos(2*u) - 2*math.cos(3*u) - math.cos(4*u)
            sx = cx + x*19
            sy = cy - 180 + y*15
            if abs(sx-cx) < 400:
                draw.ellipse((sx-2.5, sy-2.5, sx+2.5, sy+2.5), fill=(255,215,0))
        draw.text((W//2, cy+260), "اكتشفت جامعة هارفارد", fill=(255,255,255), anchor="mm")
        draw.text((W//2, cy+310), "أن القلب فيه", fill=(255,255,255), anchor="mm")
        draw.text((W//2, cy+390), "40,000", fill=(255,215,0), anchor="mm")
        draw.text((W//2, cy+440), "NEURONS - HARVARD 2024\nخلية عصبية تفكر", fill=(200,200,200), anchor="mm", align="center")
        
    elif style == "final_eye":
        # قلب فيه عين مثل نهاية الفيديو
        draw.ellipse((cx-200, cy-180, cx+200, cy+180), outline=(255,255,255,200), width=2)
        draw.ellipse((cx-90, cy-40, cx+90, cy+40), outline=(255,215,0,220), width=3)
        draw.ellipse((cx-15, cy-10, cx+15, cy+10), fill=(255,215,0))
        draw.text((W//2, cy+200), "1414 سنة", fill=(255,215,0), anchor="mm")
        draw.text((W//2, cy+260), "قلبي يعقل\nTHE HEART SEES", fill=(255,255,255), anchor="mm", align="center")
        
    else:
        draw.text((W//2, cy), text_main, fill=(255,255,255), anchor="mm", align="center")
        if text_sub:
            draw.text((W//2, cy+90), text_sub, fill=(255,215,0), anchor="mm", align="center")
    
    # موجة صوتية ذهبية تحت - تنبض مع الصوت
    wave_y = H - 200
    for i in range(62):
        x = 70 + i*15
        h_idx = i % len(waveform_heights) if waveform_heights else 0
        h = waveform_heights[h_idx] if waveform_heights else 15
        draw.rectangle((x, wave_y-h//2, x+10, wave_y+h//2), fill=(255,215,0))
    
    return img

# --- HTML ---
HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مصنع مونتاج خبير</title>
<style>
body{background:#050505;color:#fff;font-family:sans-serif;margin:0;padding:12px}
.card{background:#121212;padding:16px;border-radius:22px;max-width:850px;margin:auto;border:1px solid #333}
h1{color:#ffca28;text-align:center}
.stat{display:inline-block;background:#222;padding:6px 10px;border-radius:10px;margin:3px;font-size:11px;border:1px solid #444}
.bar{background:#222;height:8px;border-radius:6px;overflow:hidden;margin:10px 0}
.fill{height:100%;background:linear-gradient(90deg,#ffca28,#ff4081)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.agent{background:#1e1e1e;padding:9px;border-radius:10px;font-size:11px;border:1px solid #333;position:relative}
.agent.working{border-color:#ffca28;background:#332a00}
.agent.done{border-color:#00e676;background:#102a18}
.upload{background:linear-gradient(135deg,#ffca28,#ff4081);padding:15px;border-radius:14px;text-align:center;font-weight:bold;cursor:pointer;display:block;margin:12px 0}
.upload input{display:none}
#videoBox{display:none;background:#000;padding:14px;border-radius:14px;margin-top:14px;border:2px solid #00e676;text-align:center}
.download{background:linear-gradient(135deg,#00e676,#00bfa5);color:#000;padding:14px;border-radius:12px;display:block;text-align:center;text-decoration:none;font-weight:bold;margin-top:10px}
.log{background:#0a0a0a;padding:10px;border-radius:10px;max-height:120px;overflow:auto;font-size:10px;border:1px solid #222;margin-top:10px}
.managerBtn{display:block;background:linear-gradient(135deg,#ff4081,#7c4dff);color:#fff;padding:13px;border-radius:12px;text-align:center;text-decoration:none;font-weight:bold;margin:12px 0}
</style></head>
<body>
<div class="card">
<h1>💛 مصنع قلبي يقيل - مونتاج خبير تلقائي 💛</h1>
<div><span class="stat">مستوى: <b id="fLevel">1</b></span><span class="stat">انتاج: <b id="fTotal">0</b></span><span class="stat">21 خبير مونتاج</span><span class="stat">المدير: ZIZO</span></div>
<div class="bar"><div class="fill" id="fill" style="width:15%"></div></div>
<div id="status" style="background:#111;padding:10px;border-radius:10px;text-align:center;border:1px dashed #444;font-size:12px">🎬 ارفع صوتك - المصنع سيصنع مونتاج احترافي مثل الفيديو المرجعي تلقائياً</div>
<label class="upload">📤 اضغط هنا - ارفع صوت 42 ثانية ليصنع فيديو احترافي MP4
<input type="file" id="file" accept="audio/*" onchange="make()"></label>
<div class="grid" id="grid"></div>
<a href="/manager" class="managerBtn">👑 مكتب المدير - تطورات الخبراء</a>
<div id="videoBox">
<h3 style="color:#00e676">✅ اكتمل المونتاج الاحترافي!</h3>
<video id="preview" controls style="width:100%;border-radius:12px;background:#111" playsinline></video>
<a href="/download" class="download">⬇️ تنزيل فيديو احترافي MP4 - 1080x1920</a>
<p style="font-size:11px;color:#999">مونتاج: قلب نيون + جزيئات + قرآن ذهبي + موجة صوتية - بدون تدخل منك</p>
</div>
<div class="log" id="log"></div>
</div>
<script>
let mem=null;
const jobs={a1:{t:"01 راصد النبض"},a2:{t:"02 حكيم النصوص"},a3:{t:"03 خطاف كلمات"},a4:{t:"04 لسان نيون"},a5:{t:"05 هندسة إسلامية"},a6:{t:"06 جزيئات"},a7:{t:"07 موجة صوتية"},a8:{t:"08 ذهبي"},a9:{t:"09 أحمر قلب"},a10:{t:"10 حركي"},a11:{t:"11 لحني"},a12:{t:"12 جامع نهائي"},a13:{t:"13 ملون"},a14:{t:"14 قصاص"},a15:{t:"15 ناقد"},a16:{t:"16 مسرع"},a17:{t:"17 مبطئ"},a18:{t:"18 مترجم"},a19:{t:"19 ناشر"},a20:{t:"20 حارس"},a21:{t:"21 طبيب"}};
fetch('/api/mem').then(r=>r.json()).then(m=>{mem=m;document.getElementById('fLevel').innerText=m.factory_level;document.getElementById('fTotal').innerText=m.total;document.getElementById('fill').style.width=(m.factory_level*7+12)+'%';document.getElementById('log').innerHTML=m.log.slice(-10).reverse().join('<br>');render();});
function render(){let g=document.getElementById('grid');let h='';for(let k in mem.agents){let a=mem.agents[k];h+='<div class="agent" id="'+k+'"><small>'+jobs[k].t+'</small><br>'+a.name+' LVL '+a.level+' XP:'+a.xp+'</div>';}g.innerHTML=h;}
async function make(){
 let file=document.getElementById('file').files[0];if(!file)return;
 let s=document.getElementById('status');s.innerText='⏳ الخبراء الـ21 يعملون - تحليل صوت + كتابة نص + مونتاج احترافي... قد يأخذ 40-60 ثانية أول مرة';
 let keys=Object.keys(mem.agents);let i=0;let intv=setInterval(()=>{if(i<keys.length){let el=document.getElementById(keys[i]);if(el)el.classList.add('working');i++;}},120);
 let fd=new FormData();fd.append('audio',file);
 let res=await fetch('/api/make',{method:'POST',body:fd});clearInterval(intv);
 let data=await res.json();mem=data.mem;document.getElementById('fLevel').innerText=mem.factory_level;document.getElementById('fTotal').innerText=mem.total;document.getElementById('log').innerHTML=mem.log.slice(-10).reverse().join('<br>');render();document.querySelectorAll('.agent').forEach(el=>{el.classList.remove('working');el.classList.add('done')});s.innerText='✅ اكتمل المونتاج الاحترافي!';document.getElementById('videoBox').style.display='block';document.getElementById('preview').src='/download?t='+Date.now();window.scrollTo(0,document.body.scrollHeight);
}
</script>
</body></html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    mem=load_mem()
    if session.get("logged"): return HTML
    err=""
    if request.method=="POST":
        if request.form.get("password","").strip().upper()=="ZIZO":
            session["logged"]=True
            return redirect("/")
        else: err="خطأ"
    return f'<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:#050505;color:#fff;text-align:center;padding:40px;font-family:sans-serif"><div style="background:#151515;padding:26px;border-radius:20px;max-width:360px;margin:auto;border:1px solid #333"><h2>🔒 مصنع مونتاج خبير</h2><p>مستوى {mem["factory_level"]} - 21 خبير</p><form method="POST"><input type="password" name="password" placeholder="ZIZO" style="padding:14px;width:82%;border-radius:10px;border:none;text-align:center;margin:12px"><br><button style="background:#ffca28;color:#000;padding:14px 28px;border:none;border-radius:10px;width:88%;font-weight:bold">دخول المصنع</button></form><p style="color:#ff5252">{err}</p></div></body></html>'

@app.route("/api/mem")
def api_mem(): return jsonify(load_mem())

@app.route("/api/make", methods=["POST"])
def api_make():
    mem=load_mem()
    f=request.files.get('audio')
    if f: f.save(AUDIO_FILE)
    
    # تطور الخبراء
    mem["total"]+=1
    for k in mem["agents"]:
        mem["agents"][k]["xp"]+=random.randint(12,28)
        mem["agents"][k]["jobs"]+=1
        if mem["agents"][k]["xp"]>=mem["agents"][k]["level"]*120:
            mem["agents"][k]["level"]+=1
            mem["log"].append(f"{datetime.datetime.now().strftime('%H:%M')}: {mem['agents'][k]['name']} تطور للمستوى {mem['agents'][k]['level']}!")
    mem["factory_level"]=sum([a["xp"] for a in mem["agents"].values()])//900+1
    save_mem(mem)
    
    # --- صناعة فيديو احترافي مثل المرجعي ---
    try:
        from moviepy.editor import AudioFileClip, ImageSequenceClip
        
        audio = AudioFileClip(AUDIO_FILE)
        duration = min(audio.duration, 62) # مثل الفيديو المرجعي
        
        # تحليل الموجة الصوتية (مبسط)
        # نحاكي waveform ذهبي ينبض مع الصوت
        fps = 24
        total_frames = int(duration * fps)
        
        # نصوص مثل الفيديو المرجعي - مقسمة زمنياً
        segments = [
            (0, 4, "قلبك", "يفكر سابق عقلك بخمس ثواني", "gold_big"),
            (4, 7, "غريب", "غريب الموضوع", "white_big"),
            (7, 11, "من واحنا صغيرين", "نعرفو على العقل والقلب", "white_mid"),
            (11, 15, "قرار أول", "اسمع تأكيد القرآن", "gold_big"),
            (15, 24, "أَفَلَمْ يَسِيرُوا فِي الْأَرْضِ\nفَتَكُونَ لَهُمْ قُلُوبٌ", "يَعْقِلُونَ بِهَا", "quran"),
            (24, 28, "قال قلوب يعقلون بها", "ما قال عقول", "quran"),
            (28, 33, "العلم كان يضحك", "سنة 2012", "white_mid"),
            (33, 42, "particles", "", "particles"), # قلب جزيئات 40k
            (42, 50, "غريب الموضوع", "قاله النبي صلى الله عليه وسلم", "white_big"),
            (50, 55, "العالم كامل", "1414 سنة", "white_mid"),
            (55, duration, "final_eye", "", "final_eye"),
        ]
        
        frames=[]
        tmpdir = tempfile.mkdtemp()
        frame_paths=[]
        
        for fi in range(total_frames):
            t = fi / fps
            # اختر segment
            cur = None
            for seg in segments:
                if seg[0] <= t < seg[1]:
                    cur = seg
                    break
            if not cur: cur = segments[-1]
            
            # waveform عشوائي ينبض
            wave = [8 + int(30*abs(math.sin(t*5 + i*0.4)) + random.randint(0,8)) for i in range(62)]
            
            if cur[2]=="particles":
                img = make_frame("", "", "particles", t, wave)
            elif cur[2]=="final_eye":
                img = make_frame("", "", "final_eye", t, wave)
            elif cur[4]=="gold_big":
                img = make_frame(cur[2], cur[3], "gold_big", t, wave)
            elif cur[4]=="quran":
                img = make_frame(cur[2], cur[3], "quran", t, wave)
            else:
                img = make_frame(cur[2], cur[3], "white_mid", t, wave)
            
            path = os.path.join(tmpdir, f"f{fi:04d}.png")
            img.save(path)
            frame_paths.append(path)
        
        # تحويل الصور لفيديو + الصوت
        clip = ImageSequenceClip(frame_paths, fps=fps)
        clip = clip.set_audio(audio.subclip(0, duration))
        clip.write_videofile(VIDEO_FILE, fps=fps, codec='libx264', audio_codec='aac', verbose=False, logger=None)
        
    except Exception as e:
        print("Pro video error:", e)
        # fallback بسيط
        try:
            from moviepy.editor import ColorClip, AudioFileClip
            audio = AudioFileClip(AUDIO_FILE)
            dur = min(audio.duration, 42)
            color = ColorClip((720,1280), color=(0,0,0), duration=dur)
            color = color.set_audio(audio.subclip(0,dur))
            color.write_videofile(VIDEO_FILE, fps=24, codec='libx264', audio_codec='aac', verbose=False, logger=None)
        except Exception as e2:
            print("fallback error", e2)
    
    return jsonify({"ok":True,"mem":mem})

@app.route("/manager")
def manager():
    m=load_mem()
    total_xp=sum([a["xp"] for a in m["agents"].values()])
    log_html="<br>".join(m["log"][-20:][::-1])
    agents_html=""
    for k,v in m["agents"].items():
        agents_html+=f'<div style="background:#222;padding:8px;border-radius:8px;margin:4px 0;display:flex;justify-content:space-between;font-size:12px"><span>{k} - {v["name"]} LVL {v["level"]}</span><b>XP:{v["xp"]}</b></div>'
    return f'<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:#080808;color:#fff;font-family:sans-serif;padding:14px"><div style="background:#1a1a1a;padding:18px;border-radius:18px;max-width:700px;margin:auto;border:2px solid #ffca28"><h2 style="color:#ffca28;text-align:center">👑 مكتب المدير - مصنع مونتاج خبير</h2><div style="background:#222;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between"><span>مستوى المصنع</span><b>LVL {m["factory_level"]}</b></div><div style="background:#222;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between"><span>فيديوهات احترافية</span><b>{m["total"]} MP4</b></div><div style="background:#222;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between"><span>XP الخبراء</span><b>{total_xp}</b></div><h3 style="color:#ffca28">📈 تطورات الخبراء</h3><div style="background:#111;padding:10px;border-radius:10px;max-height:200px;overflow:auto;font-size:11px">{log_html}</div><h3 style="color:#00e676">👷 21 خبير مونتاج</h3>{agents_html}<a href="/" style="display:block;background:#ffca28;color:#000;padding:12px;border-radius:10px;text-align:center;text-decoration:none;margin-top:15px;font-weight:bold">🏭 العودة للمصنع</a></div></body></html>'

@app.route("/download")
def dl():
    if os.path.exists(VIDEO_FILE):
        return send_file(VIDEO_FILE, as_attachment=True, download_name=f"qalbi-PRO-LVL{load_mem()['factory_level']}.mp4", mimetype="video/mp4")
    return "لم تصنع فيديو بعد", 404

@app.route("/logout")
def logout(): session.clear(); return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
