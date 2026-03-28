# ใช้ Python version เล็กๆ
FROM python:3.9-slim

# ตั้งค่าโฟลเดอร์ทำงาน
WORKDIR /app

# ก๊อปปี้ไฟล์ข้อความ dependencies และติดตั้ง Library
COPY requirements.txt .
RUN pip install -r requirements.txt

# ก๊อปปี้โค้ดแอปพลิเคชันหลัก
COPY app.py .

# เปิดพอร์ต 5000
EXPOSE 5000

# คำสั่งรันแอป
CMD ["python", "app.py"]