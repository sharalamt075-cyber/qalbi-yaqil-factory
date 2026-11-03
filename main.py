from flask import Flask, request, session, redirect, send_file, jsonify
import os, io, json, random, datetime
from PIL import Image, ImageDraw
app = Flask(__name__)
app.secret_key = "zizo-final-21-manager-complete"

MEMORY_FILE = "/tmp/factory_memory_final.json"
def load_memory():
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE,'r') as f: return json.load(f)
    except: pass
    agents = {}
    names = ["راصد","حكيم","خطاف","لسان","مدقق","ميقاتي","صافي","ذهبي","أحمر","حركي","لحني","جامع","ملون","قصاص","ناقد","مسرع","مبطئ","مترجم","ناشر","حارس","طبيب"]
    for i,n in enumerate(names,1):
        agents[f"a{i}"]={"name":n,"level":1,"xp":0,"jobs":0}
    agents["a21"]["level"]=5
    agents["a21"]["xp"]=100
    return {"total_videos":0,"factory_level":1,"agents":agents,"log":["2026-11-03 12:00: ولادة المصنع الكامل 21 عامل - المستوى 1 - المدير ZIZO"]}

def save_memory(m):
    try:
        with open(MEMORY_FILE,'w') as f: json.dump(m,f)
    except: pass

def evolve():
    m=load_memory()
    m["total_videos"]+=1
    for k in m["agents"]:
        m["agents"][k]["xp"]+=random.randint(8,25)
        m["agents"][k]["jobs"]+=1
        if m["agents"][k]["xp"]>=m["agents"][k]["level"]*100:
            m["agents"][k]["level"]+=1
            m["log"].append(f"{datetime.datetime.now().strftime('%H:%M')}: {m['agents'][k]['name']} تطور للمستوى {m['agents'][k]['level']}!")
    m["factory_level"]=sum([a["xp"] for a in m["agents"].values()])//800+1
    if m["total_videos"]%3==0:
        m["log"].append(f"{datetime.datetime.now().strftime('%H:%M')}: إنجاز - المصنع أنتج {m['total_videos']} فيديو!")
    save_memory(m)
    return m

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مصنع قلبي يقيل - 21 عامل - مكتب المدير</title>
<style>
body{background:#060606;color:#fff;font-family:sans-serif;margin:0;padding:10px}
.card{background:#151515;padding:15px;border-radius:20px;max-width:800px;margin:auto;border:1px solid #333}
h1{color:#ff4081;text-align:center;margin:5px}.stats{display:flex;gap:6px;justify-content:center;flex-wrap:wrap}
.stat{background:#222;padding:7px 10px;border-radius:10px;font-size:11px;border:1px solid #
