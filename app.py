from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# 🌟 ฐานข้อมูลจำลอง
goldfish_db = [
    {
        "id": 1, 
        "name": "Ranchu เกรดประกวด", 
        "price": 1500, 
        "desc": "ลำตัวสั้นกลม วุ้นหนา สีส้มสด สุขภาพแข็งแรง",
        "url": "https://www.hepper.com/wp-content/uploads/2022/09/goldfish-Ranchu_bluehand_shutterstock-2.jpg",
        "is_sold": False
    }
]
next_id = 2

# 🌟 โครงสร้างหน้าเว็บ HTML + CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Goldfish Marketplace</title>
    <style>
        body { background-color: #121212; color: white; font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        .header { margin-bottom: 20px; }
        .search-box { margin-bottom: 30px; }
        .search-box input { padding: 10px; width: 300px; border-radius: 5px; border: none; font-size: 16px;}
        .form-container { background: #1e1e1e; padding: 20px; border-radius: 10px; display: inline-block; margin-bottom: 30px; border: 1px solid #333; }
        input, textarea { padding: 8px; margin: 5px; border-radius: 5px; border: none; width: 90%; }
        button { padding: 10px 15px; border-radius: 5px; border: none; cursor: pointer; font-weight: bold; margin: 5px; }
        .btn-search { background-color: #008CBA; color: white; }
        .btn-sell { background-color: #4CAF50; color: white; width: 95%; margin-top: 10px;}
        .btn-buy { background-color: #ff9800; color: white; width: 100%; font-size: 16px;}
        .btn-delete { background-color: #F44336; color: white; padding: 5px 10px; font-size: 12px; }
        .btn-edit { background-color: #FFC107; color: black; padding: 5px 10px; font-size: 12px; }
        .gallery { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .card { background: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; width: 300px; text-align: left; position: relative; }
        .card img { width: 100%; height: 200px; object-fit: cover; border-radius: 10px; }
        .price { color: #4CAF50; font-size: 22px; font-weight: bold; margin: 10px 0; }
        .desc { font-size: 14px; color: #bbb; height: 40px; overflow: hidden; }
        .sold-out { opacity: 0.5; }
        .sold-stamp { position: absolute; top: 80px; left: 50px; color: red; border: 3px solid red; padding: 10px; font-size: 30px; font-weight: bold; transform: rotate(-20deg); }
        .edit-box { display: flex; gap: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐟 GOLDFISH MARKETPLACE</h1>
        <p>ตลาดซื้อขายปลาทองออนไลน์</p>
    </div>

    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="ค้นหาชื่อ หรือ รายละเอียด..." value="{{ request.args.get('q', '') }}">
            <button type="submit" class="btn-search">🔍 ค้นหา</button>
            <a href="/"><button type="button" style="background:#555; color:white;">เคลียร์</button></a>
        </form>
    </div>

    <div class="form-container">
        <h3>📢 ลงขายปลาทองของคุณ</h3>
        <form action="{{ url_for('sell_fish') }}" method="POST">
            <input type="text" name="name" placeholder="ชื่อสายพันธุ์ / หัวข้อ" required><br>
            <input type="number" name="price" placeholder="ราคา (บาท)" required><br>
            <input type="url" name="url" placeholder="ลิงก์รูปภาพ (URL)" required><br>
            <textarea name="desc" placeholder="รายละเอียดปลาทอง..." required></textarea><br>
            <button type="submit" class="btn-sell">💰 ประกาศขาย</button>
        </form>
    </div>

    <div class="gallery">
        {% for fish in fishes %}
        <div class="card {% if fish.is_sold %}sold-out{% endif %}">
            <img src="{{ fish.url }}" alt="Goldfish">
            {% if fish.is_sold %}
                <div class="sold-stamp">SOLD OUT</div>
            {% endif %}
            
            <h3>{{ fish.name }}</h3>
            <div class="price">฿{{ fish.price }}</div>
            <p class="desc">{{ fish.desc }}</p>
            
            {% if not fish.is_sold %}
            <form action="{{ url_for('buy_fish', fish_id=fish.id) }}" method="POST">
                <button type="submit" class="btn-buy">🛒 สั่งซื้อเลย</button>
            </form>
            {% else %}
            <button class="btn-buy" style="background:#555; cursor:not-allowed;" disabled>สินค้าหมด</button>
            {% endif %}

            <form action="{{ url_for('edit_image', fish_id=fish.id) }}" method="POST" class="edit-box">
                <input type="url" name="new_url" placeholder="วางลิงก์รูปล่าสุดที่นี่..." required style="width: 65%; font-size: 11px;">
                <button type="submit" class="btn-edit">🖼️ เปลี่ยนรูป</button>
            </form>

            <form action="{{ url_for('delete_fish', fish_id=fish.id) }}" method="POST" style="margin-top: 5px; text-align:center;">
                <button type="submit" class="btn-delete">🗑️ ลบโพสต์</button>
            </form>
        </div>
        {% else %}
            <p style="color:#ff9800;">ไม่มีปลาทองที่คุณค้นหา ลองคำอื่นดูนะ!</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Route: หน้าแรก และ ระบบค้นหา
@app.route("/")
def index():
    query = request.args.get("q", "").lower()
    if query:
        filtered_fishes = [f for f in goldfish_db if query in f["name"].lower() or query in f["desc"].lower()]
    else:
        filtered_fishes = goldfish_db
    return render_template_string(HTML_TEMPLATE, fishes=filtered_fishes)

# Route: ลงขาย (Create)
@app.route("/sell", methods=["POST"])
def sell_fish():
    global next_id
    name = request.form.get("name")
    price = request.form.get("price")
    url = request.form.get("url")
    desc = request.form.get("desc")
    
    goldfish_db.append({
        "id": next_id, 
        "name": name, 
        "price": price, 
        "desc": desc, 
        "url": url, 
        "is_sold": False
    })
    next_id += 1
    return redirect(url_for("index"))

# Route: สั่งซื้อ (Update Status)
@app.route("/buy/<int:fish_id>", methods=["POST"])
def buy_fish(fish_id):
    for fish in goldfish_db:
        if fish["id"] == fish_id:
            fish["is_sold"] = True
            break
    return redirect(url_for("index"))

# Route: แก้ไขรูปภาพ (Update Image URL)
@app.route("/edit_image/<int:fish_id>", methods=["POST"])
def edit_image(fish_id):
    new_url = request.form.get("new_url")
    for fish in goldfish_db:
        if fish["id"] == fish_id:
            fish["url"] = new_url
            break
    return redirect(url_for("index"))

# Route: ลบข้อมูล (Delete)
@app.route("/delete/<int:fish_id>", methods=["POST"])
def delete_fish(fish_id):
    global goldfish_db
    goldfish_db = [f for f in goldfish_db if f["id"] != fish_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)