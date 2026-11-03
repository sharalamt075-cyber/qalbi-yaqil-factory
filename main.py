from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>قلبي يقيل - مصنع</title>
<style>
body { font-family: sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 50px; }
.card { background: #1e1e1e; padding: 30px; border-radius: 20px; max-width: 500px; margin: auto; }
h1 { color: #ff4081; }
.btn { background: #ff4081; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; display: inline-block; margin-top: 20px; font-size: 18px; }
.green { color: #00e676; font-weight: bold; }
</style>
</head>
<body>
<div class="card">
<h1>💖 قلبي يقيل</h1>
<h2>مصنعك يعمل الآن!</h2>
<p class="green">● Live - Online 24/7</p>
<p>هذا موقع مصنعك على Render</p>
<p>الرابط: qalbi-yaqil-factory.onrender.com</p>
<a class="btn" href="#">دخول المصنع</a>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
