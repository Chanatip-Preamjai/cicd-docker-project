import app

def test_index_page():
    client = app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"MARKETPLACE" in response.data

def test_sell_fish():
    client = app.app.test_client()
    data = {
        "name": "Test Oranda", 
        "price": "500", 
        "url": "http://test.com/img.jpg",
        "desc": "ปลาเทสต์ระบบ"
    }
    response = client.post("/sell", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Oranda" in response.data
    assert b"500" in response.data

def test_search_fish():
    client = app.app.test_client()
    response = client.get("/?q=Ranchu")
    assert response.status_code == 200
    assert b"Ranchu" in response.data

def test_edit_image():
    client = app.app.test_client()
    # ลองเปลี่ยนรูปภาพของปลาทองตัวแรก (id=1)
    new_img_url = "http://test.com/new_goldfish.jpg"
    response = client.post("/edit_image/1", data={"new_url": new_img_url}, follow_redirects=True)
    assert response.status_code == 200
    assert new_img_url.encode('utf-8') in response.data