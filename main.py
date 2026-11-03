from flask import Flask, request, session, redirect, send_file, jsonify
import os, json, math, random, tempfile
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)
app.secret_key = "zizo-v6-trend-factory"

MEM_FILE="/tmp/mem.json"
VIDEO_FILE="/tmp/qalbi.mp4"
AUDIO_FILE="/tmp/in.mp3"

def load_mem():
    try:
        if os.path.exists(MEM_FILE):
            with open(MEM_FILE,'r') as f: return json.load(f)
    except: pass
    return {"total":0,"trends_invented":0}

def save_mem(m):
    with open(MEM_FILE,'w') as f: json.dump(m,f)

def get_font(size, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,size)
            except: pass
    return ImageFont.load_default()

class CapCutProEngine:
    def __init__(self):
        self.W, self.H = 1080,1920
        self.cx, self.cy = 540,820
        self.trending_styles = ["heart_neon_gold","quran_gold_frame","particles_40k","eye_in_heart","negativity_text_pop","islamic_mandala"]
    
    def invent_trend(self, audio_text, t):
        if "جرح" in audio_text or "تنسى" in audio_text:
            return "heart_neon_gold"
        elif "قلب" in audio_text or "يعقل" in audio_text:
            return "quran_gold_frame"
        elif "40" in audio_text or "خلية" in audio_text:
            return "particles_40k"
        elif "عين" in audio_text or "يرى" in audio_text:
            return "eye_in_heart"
        else:
            return random.choice(self.trending_styles)

    def add_islamic_mandala(self, draw, t):
        for r in [300,540,820]:
            for i in range(32):
                ang = i*360/32 + t*(7 if r%2==0 else -5)
                x = self.cx + r*math.cos(math.radians(ang))
                y = self.cy + r*math.sin(math.radians(ang))
                draw.ellipse((x-2,y-2,x+2,y+2), fill=(255,215,0,38))
            for i in range(12):
                a1=i*360/12 + t*2
                a2=(i+4)*360/12 + t*2
                x1=self.cx+r*math.cos(math.radians(a1)); y1=self.cy+r*math.sin(math.radians(a1))
                x2=self.cx+r*math.cos(math.radians(a2)); y2=self.cy+r*math.sin(math.radians(a2))
                if r==540:
                    draw.line((x1,y1,x2,y2), fill=(255,215,0,28), width=1)

    def add_heart_neon(self, draw, t):
        pulse = 1.0 + 0.09*math.sin(t*3.3)
        base = 300*pulse
        for glow, alpha, w in [(95,12,2),(70,22,2),(45,40,3),(20,85,4)]:
            rr=base+glow
            draw.ellipse((self.cx-rr, self.cy-rr*0.92, self.cx+rr, self.cy+rr*0.92), outline=(255,215,0,alpha), width=w)
        draw.ellipse((self.cx-base, self.cy-base*0.92, self.cx+base, self.cy+base*0.92), outline=(255,240,130,255), width=6)

    def add_particles_heart(self, draw, t, cx, cy):
        for _ in range(180):
            u = random.random()*2*math.pi
            x = 16*(math.sin(u)**3)
            y = 13*math.cos(u) - 5*math.cos(2*u) - 2*math.cos(3*u) - math.cos(4*u)
            sx = cx + x*18 + random.randint(-4,4)
            sy = cy - 200 + y*14 + random.randint(-4,4)
            if abs(sx-cx)<360:
                draw.ellipse((sx-2.2,sy-2.2,sx+2.2,sy+2.2), fill=(255,215,0,random.randint(80,255)))

    def add_waveform_pro(self, draw, t):
        wave_y=self.H-250
        for i in range(62):
            x=12 + i*17
            h=12 + int(48*abs(math.sin(t*5.4 + i*0.42)) + random.randint(2,14))
            draw.rectangle((x, wave_y-h, x+11, wave_y+h), fill=(255,215,0,230))
            draw.rectangle((x, wave_y-h, x+11, wave_y-h+4), fill=(255,255,200,200))

    def render_trending_frame(self, text1, text2, t, trend_style):
        W,H=self.W,self.H
        img=Image.new('RGB',(W,H),(6,6,10))
        draw=ImageDraw.Draw(img,'RGBA')
        self.add_islamic_mandala(draw,t)
        if trend_style in ["heart_neon_gold","quran_gold_frame","negativity_text_pop"]:
            self.add_heart_neon(draw,t)
        elif trend_style=="particles_40k":
            self.add_heart_neon(draw,t)
            self.add_particles_heart(draw,t,self.cx,self.cy)
        f_big=get_font(78,True)
        f_mid=get_font(56,True)
        if trend_style=="particles_40k":
            draw.text((self.cx, self.cy-280), text1, font=get_font(52,True), fill=(255,255,255), anchor="mm", stroke_width=2, stroke_fill=(0,0,0))
            draw.text((self.cx, self.cy+10), "40,000", font=get_font(108,True), fill=(255,215,0), anchor="mm", stroke_width=3, stroke_fill=(0,0,0))
            draw.text((self.cx, self.cy+110), text2, font=f_mid, fill=(255,255,255), anchor="mm")
        elif trend_style=="eye_in_heart":
            draw.ellipse((self.cx-110,self.cy-55,self.cx+110,self.cy+55), outline=(255,255,255,230), width=3)
            draw.ellipse((self.cx-18,self.cy-12,self.cx+18,self.cy+12), fill=(255,215,0))
            draw.text((self.cx, self.cy+180), text1, font=f_big, fill=(255,215,0), anchor="mm", stroke_width=3, stroke_fill=(0,0,0))
            draw.text((self.cx, self.cy+260), text2, font=f_mid, fill=(255,255,255), anchor="mm")
        else:
            draw.text((self.cx+4, self.cy-55+4), text1, font=f_big, fill=(0,0,0,200), anchor="mm")
            draw.text((self.cx, self.cy-55), text1, font=f_big, fill=(255,255,255), anchor="mm", stroke_width=3, stroke_fill=(170,130,0))
            draw.text((self.cx+3, self.cy+45+3), text2, font=f_mid, fill=(0,0,0,200), anchor="mm")
            col=(255,215,0) if "جرحتك" in text2 or "زينة" in text2 else (255,255,255)
            draw.text((self.cx, self.cy+45), text2, font=f_mid, fill=col, anchor="mm", stroke_width=2, stroke_fill=(0,0,0))
        draw.text((W//2, 108), "قلبي يقيل ♡", font=get_font(48,True), fill=(255,215,0), anchor="mm")
        self.add_waveform_pro(draw,t)
        for _ in range(30):
            x=random.randint(self.cx-320,self.cx+320)
            y=random.randint(self.cy-320,self.cy+320)
            if math.hypot(x-self.cx,y-self.cy)<360:
                draw.ellipse((x-1,y-1,x+1,y+1), fill=(255,215,0,random.randint(50,150)))
        return img

capcut = CapCutProEngine()

HTML="""
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>V6 Trend Factory</title>
<style>
body{background:#07070c;color:#fff;font-family:sans-serif;padding:0;margin:0}
.card{background:#121216;padding:18px;border-radius:22px;max-width:840px;margin:14px auto;border:2px solid #ffca28}
h1{color:#ffca28;text-align:center}
.badge{display:inline-block;background:#222;padding:6px 12px;border-radius:20px;margin:4px;font-size:12px;border:1px solid #444}
.upload{background:linear-gradient(135deg,#ffca28,#ff4081);padding:20px;border-radius:16px;text-align:center;font-weight:900;cursor:pointer;display:block;margin:16px 0;font-size:18px;color:#000}
.upload input{display:none}
.status{background:#1a1a22;padding:14px;border-radius:12px;text-align:center;border:1px solid #ffca28;margin:12px 0;line-height:1.6}
video{width:100%;border-radius:16px;background:#000;max-height:75vh}
.download{background:linear-gradient(135deg,#00e676,#00bfa5);color:#000;padding:18px;border-radius:14px;display:block;text-align:center;text-decoration:none;font-weight:900;margin-top:12px;font-size:18px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
.agent{background:#1e1e26;padding:10px;border-radius:10px;font-size:11px;border:1px solid #333}
.agent.working{border-color:#ffca28;background:#332a00}
</style></head>
<body>
<div class="card">
<h1>🤖💛 مصنع V6 - الوكلاء يخترعون الترند بأنفسهم</h1>
<div><span class="badge">🧠 CapCut Engine داخلي</span><span class="badge">✨ 6 ستايلات ترند</span><span class="badge">🤖 21 وكيل مخترع</span><span class="badge">📈 يخترعون لوحدهم</span></div>
<div id="status" class="status">🤖 الوكلاء جاهزون بأداة كاب كات احترافية<br>هم سيحللون صوتك ويخترعون الستايل الترند المناسب لوحدهم</div>
<label class="upload">📤 ارفع صوتك - الوكلاء سيخترعون فيديو ترند لوحدهم
<input type="file" id="file" accept="audio/*" onchange="upload()"></label>
<div class="grid" id="agents"></div>
<video id="preview" controls playsinline src="/download"></video>
<a href="/download" class="download">⬇️ تحميل فيديو ترند احترافي</a>
</div>
<script>
const agentsNames=["04 لسان نيون","05 هندسة إسلامية","06 جزيئات 40k","07 موجة صوتية","08 ذهبي نيون","09 أحمر قلب","10 حركي ترند","11 لحني","12 جامع نهائي"];
let grid=document.getElementById('agents');
agentsNames.forEach((n,i)=>{let d=document.createElement('div');d.className='agent';d.id='ag'+i;d.innerHTML=n;grid.appendChild(d);});
async function upload(){
 let f=document.getElementById('file').files[0];if(!f)return;
 let s=document.getElementById('status');
 s.innerHTML='🤖 الوكلاء يحللون صوتك...<br>🧠 يخترعون الترند...<br>✨ يصنعون بCapCut Engine... 35 ثانية';
 document.querySelectorAll('.agent').forEach((el,i)=>{setTimeout(()=>el.classList.add('working'), i*120);});
 let fd=new FormData();fd.append('audio',f);
 let res=await fetch('/api/make',{method:'POST',body:fd});
 s.innerHTML='✅ الوكلاء اخترعوا ترند جديد! شغل الفيديو';
 document.querySelectorAll('.agent').forEach(el=>el.classList.remove('working'));
 document.getElementById('preview').src='/download?t='+Date.now();
}
</script>
</body></html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    if session.get("logged"): return HTML
    if request.method=="POST":
        if request.form.get("password","").strip().upper()=="ZIZO":
            session["logged"]=True
            return redirect("/")
    return '<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:#050505;color:#fff;text-align:center;padding:60px"><div style="background:#151515;padding:34px;border-radius:24px;max-width:400px;margin:auto;border:2px solid #ffca28"><h2>🤖 V6 Trend Factory</h2><p style="color:#999;font-size:13px">الوكلاء لديهم CapCut Engine</p><form method="POST"><input type="password" name="password" placeholder="ZIZO" style="padding:18px;width:90%;border-radius:14px;border:none;text-align:center;margin:16px;font-size:18px"><br><button style="background:#ffca28;color:#000;padding:18px 34px;border:none;border-radius:14px;width:95%;font-weight:900;font-size:18px">دخول مصنع الترند</button></form></div></body></html>'

@app.route("/api/make", methods=["POST"])
def make():
    f=request.files.get('audio')
    if f: f.save(AUDIO_FILE)
    mem=load_mem()
    mem["total"]=mem.get("total",0)+1
    mem["trends_invented"]=mem.get("trends_invented",0)+1
    save_mem(mem)
    try:
        from moviepy.editor import AudioFileClip, ImageSequenceClip
        audio=AudioFileClip(AUDIO_FILE)
        dur=min(audio.duration, 44)
        fps=24
        total=int(dur*fps)
        chunks=[("قلّي تعرف علاش تنسى","كلمة زينة"),("ولا تنسى كلمة","وحدة جرحتك؟"),("عقلك يميل للتركيز","على الألم أكثر"),("لأنها تهديد","لبقائك"),("هذا يسمى","بانحياز السلبية"),("قلبي يقيل ♡","القلب يعقل")]
        tmpdir=tempfile.mkdtemp()
        paths=[]
        for fi in range(total):
            t=fi/fps
            idx=int((t/dur)*len(chunks))
            if idx>=len(chunks): idx=len(chunks)-1
            t1,t2=chunks[idx]
            trend_style=capcut.invent_trend(t1+" "+t2, t)
            img=capcut.render_trending_frame(t1,t2,t,trend_style)
            p=os.path.join(tmpdir,f"f{fi:04d}.jpg")
            img.save(p, quality=93)
            paths.append(p)
        clip=ImageSequenceClip(paths, fps=fps)
        clip=clip.set_audio(audio.subclip(0,dur))
        clip.write_videofile(VIDEO_FILE, fps=fps, codec='libx264', audio_codec='aac', verbose=False, logger=None)
    except Exception as e:
        print("V6 error", e)
        import traceback; traceback.print_exc()
    return jsonify({"ok":True})

@app.route("/download")
def dl():
    if os.path.exists(VIDEO_FILE): return send_file(VIDEO_FILE, mimetype="video/mp4")
    if os.path.exists(AUDIO_FILE): return send_file(AUDIO_FILE, mimetype="audio/mpeg")
    return "ارفع صوت",404

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
