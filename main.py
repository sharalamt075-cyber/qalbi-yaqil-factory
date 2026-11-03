from flask import Flask, request, session, redirect, send_file, jsonify
import os, io, json, random, datetime
from PIL import Image, ImageDraw
app = Flask(__name__)
app.secret_key = "zizo-final-fixed-2026"

MEMORY_FILE = "/tmp/factory_memory.json"

def load_memory():
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE,'r') as f:
                return json.load(f)
    except:
        pass
    agents = {}
    names = ["راصد","حكيم","خطاف","لسان","مدقق","ميقاتي","صافي","ذهبي","احمر","حركي","لحني","جامع","ملون","قصاص","ناقد","مسرع","مبطئ","مترجم","ناشر","حارس","طبيب"]
    for i,n in enumerate(names,1):
        agents["a"+str(i)] = {"name": n, "level": 1, "xp": 0, "jobs": 0}
    agents["a21"]["level"] = 5
    agents["a21"]["xp"] = 100
    return {"total_videos":0,"factory_level":1,"agents":agents,"log":["2026-11-03: ولادة المصنع 21 عامل"]}

def save_memory(m):
    try:
        with open(MEMORY_FILE,'w') as f:
            json.dump(m,f)
    except:
        pass

def do_evolve():
    m = load_memory()
    m["total_videos"] += 1
    for k in m["agents"]:
        m["agents"][k]["xp"] += random.randint(8,25)
        m["agents"][k]["jobs"] += 1
        if m["agents"][k]["xp"] >= m["agents"][k]["level"]*100:
            m["agents"][k]["level"] += 1
            m["log"].append(str(datetime.datetime.now().strftime("%H:%M")) + ": " + m["agents"][k]["name"] + " تطور للمستوى " + str(m["agents"][k]["level"]))
    m["factory_level"] = sum([a["xp"] for a in m["agents"].values()]) // 800 + 1
    save_memory(m)
    return m

HTML_PAGE = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مصنع قلبي يقيل</title>
<style>
body{background:#060606;color:#fff;font-family:sans-serif;margin:0;padding:10px}
.card{background:#151515;padding:15px;border-radius:20px;max-width:800px;margin:auto;border:1px solid #333}
h1{color:#ff4081;text-align:center}
.stats{display:flex;gap:6px;justify-content:center;flex-wrap:wrap}
.stat{background:#222;padding:7px 10px;border-radius:10px;font-size:11px;border:1px solid #444}
.stat b{color:#00e676}
.bar{background:#222;height:8px;border-radius:5px;overflow:hidden;margin:8px 0}
.fill{height:100%;background:linear-gradient(90deg,#00e676,#ff4081)}
.status{background:#111;padding:10px;border-radius:10px;text-align:center;border:1px dashed #444;font-size:12px;margin:10px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.agent{background:#222;padding:10px;border-radius:12px;font-size:11px;cursor:pointer;border:1px solid #333;position:relative}
.agent .lvl{position:absolute;top:2px;left:5px;background:#ff4081;color:#fff;font-size:8px;padding:2px 5px;border-radius:8px}
.agent.working{border-color:#ffca28;background:#332a00}
.agent.done{border-color:#00e676;background:#0f2318}
.upload{background:linear-gradient(135deg,#ff4081,#ff8a65);padding:14px;border-radius:12px;text-align:center;cursor:pointer;font-weight:bold;margin:10px 0}
.upload input{display:none}
#videoBox{display:none;background:#000;padding:12px;border-radius:12px;margin-top:12px;text-align:center;border:1px solid #00e676}
.download{background:linear-gradient(135deg,#00e676,#00bfa5);color:#000;padding:13px;border-radius:12px;display:block;text-align:center;text-decoration:none;font-weight:bold;margin-top:10px}
.log{background:#0a0a0a;padding:10px;border-radius:10px;max-height:120px;overflow:auto;font-size:10px;border:1px solid #222;margin-top:10px}
.managerBtn{display:block;background:linear-gradient(135deg,#ff4081,#7c4dff);color:white;padding:14px;border-radius:12px;text-align:center;text-decoration:none;font-weight:bold;margin:12px 0;font-size:14px}
.room{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.93);display:none;align-items:center;justify-content:center;z-index:999;padding:15px}
.roomBox{background:#1e1e1e;padding:20px;border-radius:18px;max-width:400px;width:100%;text-align:center;border:2px solid #ff4081}
</style></head>
<body>
<div class="card">
<h1>💖 قلبي يقيل - 21 عامل كامل 💖</h1>
<div class="stats">
<div class="stat">مستوى المصنع: <b id="fLevel">1</b></div>
<div class="stat">انتاج: <b id="fTotal">0</b></div>
<div class="stat">عمال: <b>21</b> غرفة</div>
<div class="stat">المدير: <b>ZIZO</b></div>
</div>
<div class="bar"><div class="fill" id="fill" style="width:10%"></div></div>
<div class="status" id="status">🎙️ مصنع كامل 21 غرفة - ارفع صوت 42 ثانية</div>
<label class="upload">📤 اضغط هنا لرفع صوت 42 ثانية
<input type="file" id="file" accept="audio/*" onchange="start()"></label>
<div class="grid" id="grid"></div>
<a href="/manager" class="managerBtn">👑 مكتب المدير - معلومات المصنع وتطورات الـ21 عامل</a>
<div id="videoBox">
<h3 style="color:#00e676">✅ اكتمل انتاج 21 عامل + تطور!</h3>
<a href="/download" class="download">⬇️ تنزيل الفيديو - مصنع LVL <span id="dl">1</span></a>
</div>
<div class="log" id="log"></div>
<div style="display:flex;gap:6px;margin-top:10px">
<a href="/reset" style="flex:1;background:#222;color:#fff;padding:10px;border-radius:10px;text-align:center;text-decoration:none;font-size:12px">تصفير</a>
<a href="/logout" style="flex:1;background:#333;color:#fff;padding:10px;border-radius:10px;text-align:center;text-decoration:none;font-size:12px">خروج</a>
</div>
</div>
<div class="room" id="room" onclick="if(event.target==this)this.style.display='none'">
<div class="roomBox">
<h2 id="rTitle"></h2>
<p id="rDesc" style="font-size:12px;color:#ccc"></p>
<div style="display:flex;gap:6px;justify-content:center"><div class="stat">LVL <b id="rLvl">1</b></div><div class="stat">XP <b id="rXp">0</b></div><div class="stat">اعمال <b id="rJobs">0</b></div></div>
<div style="font-size:45px;margin:10px" id="rIcon">⚙️</div>
<p style="color:#00e676;font-size:11px" id="rStatus"></p>
<div style="background:#111;padding:8px;border-radius:8px;font-size:10px;text-align:right;margin-top:8px" id="rEvo"></div>
<button onclick="document.getElementById('room').style.display='none'" style="background:#ff4081;color:#fff;padding:10px;border:none;border-radius:10px;width:100%;margin-top:10px">اغلاق الغرفة</button>
</div>
</div>
<script>
let mem=null;
const jobs={
a1:{t:"01 راصد - ترند",d:"يبحث في تيك توك عن ترند القلب",i:"🔍"},
a2:{t:"02 حكيم - دراسة",d:"يقرأ دراسة طبية عن القلب",i:"📚"},
a3:{t:"03 خطاف - هوك",d:"يكتب اول 3 ثواني تشد القلب",i:"🎣"},
a4:{t:"04 لسان - بلهجتك",d:"يكتب بلهجتك الموريتانية",i:"🗣️"},
a5:{t:"05 مدقق - تدقيق",d:"يصحح الاخطاء",i:"✅"},
a6:{t:"06 ميقاتي - توقيت",d:"يضبط توقيت 42 ثانية",i:"⏱️"},
a7:{t:"07 صافي - تنظيف",d:"ينظف الصوت",i:"🎧"},
a8:{t:"08 ذهبي - قلب ذهبي",d:"يصنع القلب الذهبي",i:"💛"},
a9:{t:"09 احمر - نابض",d:"يصنع الرقم 1 نابض",i:"❤️"},
a10:{t:"10 حركي - تحريك",d:"يحرك النص مع النبض",i:"🎬"},
a11:{t:"11 لحني - موسيقى",d:"يضيف موسيقى",i:"🎵"},
a12:{t:"12 جامع - مونتاج",d:"يجمع الفيديو",i:"🎞️"},
a13:{t:"13 ملون - الوان",d:"يختار الوان الترند",i:"🎨"},
a14:{t:"14 قصاص - قص",d:"يقص على مقاس تيك توك",i:"✂️"},
a15:{t:"15 ناقد - مراجعة",d:"يراجع الفيديو",i:"👀"},
a16:{t:"16 مسرع - سرعة",d:"يسرع اللقطات",i:"⚡"},
a17:{t:"17 مبطئ - تأثيرات",d:"يضيف تأثيرات",i:"🐢"},
a18:{t:"18 مترجم - ترجمة",d:"يضيف ترجمة",i:"🌐"},
a19:{t:"19 ناشر - نشر",d:"يجهز الوصف",i:"📤"},
a20:{t:"20 حارس - حماية",d:"يحمي المصنع",i:"🛡️"},
a21:{t:"21 طبيب - يحرس المصنع",d:"طبيب المصنع يحرس الـ21 عامل - صحة 100%",i:"👨‍⚕️"}
};
fetch('/api/mem').then(r=>r.json()).then(m=>{
 mem=m;
 document.getElementById('fLevel').innerText=m.factory_level;
 document.getElementById('fTotal').innerText=m.total_videos;
 document.getElementById('dl').innerText=m.factory_level;
 document.getElementById('fill').style.width=(m.factory_level*8+10)+'%';
 document.getElementById('log').innerHTML=m.log.slice(-10).reverse().join('<br>');
 render();
});
function render(){
 let g=document.getElementById('grid');let h='';
 for(let k in mem.agents){
  let a=mem.agents[k];let j=jobs[k];
  h+='<div class="agent" onclick="openRoom(\''+k+'\')" id="'+k+'"><div class="lvl">LVL '+a.level+'</div> '+j.t+'<br><small style="color:#888">XP:'+a.xp+' | '+a.jobs+' عمل</small></div>';
 }
 g.innerHTML=h;
}
function openRoom(k){
 let a=mem.agents[k];let j=jobs[k];
 document.getElementById('room').style.display='flex';
 document.getElementById('rTitle').innerText='غرفة '+j.t;
 document.getElementById('rDesc').innerText=j.d;
 document.getElementById('rLvl').innerText=a.level;
 document.getElementById('rXp').innerText=a.xp;
 document.getElementById('rJobs').innerText=a.jobs;
 document.getElementById('rIcon').innerText=j.i;
 document.getElementById('rStatus').innerText=a.level>5?'خبير متطور جدا':'يتعلم';
 document.getElementById('rEvo').innerHTML='تطوره الذاتي:<br>كل فيديو = +8-25 XP<br>المستوى '+a.level+'<br>يحتاج '+(a.level*100 - a.xp)+' XP للمستوى القادم';
}
function start(){
 let s=document.getElementById('status');
 s.innerText='🚀 المصنع 21 عامل بدأ...';
 let keys=Object.keys(mem.agents);let i=0;
 let intv=setInterval(()=>{
  if(i<keys.length){
   let el=document.getElementById(keys[i]);
   if(el){el.classList.add('working');}
   s.innerText='يعمل الآن: '+jobs[keys[i]].t;
   i++;
  } else {
   clearInterval(intv);
   fetch('/api/evolve',{method:'POST'}).then(r=>r.json()).then(nm=>{
    mem=nm;
    document.getElementById('fLevel').innerText=nm.factory_level;
    document.getElementById('fTotal').innerText=nm.total_videos;
    document.getElementById('dl').innerText=nm.factory_level;
    document.getElementById('fill').style.width=(nm.factory_level*8+10)+'%';
    document.getElementById('log').innerHTML=nm.log.slice(-10).reverse().join('<br>');
    render();
    s.innerText='✅ اكتمل المصنع الكامل! المستوى '+nm.factory_level;
    document.getElementById('videoBox').style.display='block';
   });
  }
 },250);
}
</script>
</body></html>
"""

LOGIN_HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>body{background:#060606;color:#fff;text-align:center;padding:40px;font-family:sans-serif}
.card{background:#151515;padding:25px;border-radius:18px;max-width:350px;margin:auto;border:1px solid #333}
input{padding:14px;width:80%;border-radius:10px;border:none;margin:12px;text-align:center;font-size:16px}
button{background:#ff4081;color:#fff;padding:14px 28px;border:none;border-radius:10px;font-size:16px;width:85%}</style>
</head><body><div class="card"><h2>🔒 مصنع 21 عامل</h2>
<form method="POST"><input type="password" name="password" placeholder="ZIZO"><br><button>دخول</button></form>
<p style="color:#ff5252">{err}</p></div></body></html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    mem = load_memory()
    if session.get("logged"):
        return HTML_PAGE
    err = ""
    if request.method == "POST":
        if request.form.get("password","").strip().upper() == "ZIZO":
            session["logged"] = True
            return redirect("/")
        else:
            err = "خطأ - اكتب ZIZO"
    return LOGIN_HTML.replace("{err}", err)

@app.route("/api/mem")
def api_mem():
    return jsonify(load_memory())

@app.route("/api/evolve", methods=["POST"])
def api_evolve():
    return jsonify(do_evolve())

@app.route("/manager")
def manager_page():
    m = load_memory()
    total_xp = sum([a["xp"] for a in m["agents"].values()])
    log_html = "<br>".join(m["log"][-20:][::-1])
    agents_html = ""
    for k,v in m["agents"].items():
        agents_html += '<div style="background:#222;padding:8px;border-radius:8px;margin:4px 0;display:flex;justify-content:space-between;font-size:12px"><span>'+k+' - '+v["name"]+' LVL '+str(v["level"])+'</span><b>XP:'+str(v["xp"])+'</b></div>'
    return '''
    <html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مكتب المدير</title>
    <style>body{background:#080808;color:#fff;font-family:sans-serif;padding:15px}
    .card{background:#1a1a1a;padding:18px;border-radius:18px;max-width:700px;margin:auto;border:2px solid #ff4081}
    .stat{background:#222;padding:10px;border-radius:10px;margin:6px 0;display:flex;justify-content:space-between}
    b{color:#00e676} h2{color:#ff4081;text-align:center}</style>
    </head><body><div class="card">
    <h2>👑 مكتب المدير ZIZO</h2>
    <div class="stat"><span>مستوى المصنع</span><b>LVL '''+str(m["factory_level"])+'''</b></div>
    <div class="stat"><span>فيديوهات</span><b>'''+str(m["total_videos"])+'''</b></div>
    <div class="stat"><span>مجموع XP</span><b>'''+str(total_xp)+'''</b></div>
    <div class="stat"><span>العمال</span><b>21 عامل</b></div>
    <h3 style="color:#ffca28">📈 سجل التطورات</h3>
    <div style="background:#111;padding:10px;border-radius:10px;max-height:200px;overflow:auto;font-size:11px">'''+log_html+'''</div>
    <h3 style="color:#00e676">👷 معلومات العمال</h3>'''+agents_html+'''
    <div style="display:flex;gap:8px;margin-top:15px">
    <a href="/" style="flex:1;background:#ff4081;color:#fff;padding:12px;border-radius:10px;text-align:center;text-decoration:none">🏭 المصنع</a>
    <a href="/logout" style="flex:1;background:#333;color:#fff;padding:12px;border-radius:10px;text-align:center;text-decoration:none">خروج</a>
    </div></div></body></html>
    '''

@app.route("/download")
def dl():
    m = load_memory()
    img = Image.new('RGB', (720, 1280), color=(15, 15, 30))
    d = ImageDraw.Draw(img)
    d.text((140,500), "قلبي يقيل - 21 عامل", fill=(255,64,129))
    d.text((120,560), "LVL "+str(m["factory_level"])+" - "+str(m["total_videos"])+" فيديو", fill=(0,230,118))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="qalbi-21-LVL"+str(m["factory_level"])+".png", mimetype="image/png")

@app.route("/reset")
def reset():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
