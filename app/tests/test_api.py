from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Test the total_spent endpoint (GET /total_spent)
def test_total_spent():
    response = client.get("/total_spent?start_date=2025-01-01&end_date=2025-01-31")
    assert response.status_code == 200
    # Adjust the expected total_spent based on your test data
    assert "total_spent" in response.json()


# Test the top_products endpoint (GET /top_products)
def test_top_products():
    response = client.get("/top_products?start_date=2025-01-01&end_date=2025-01-31")
    assert response.status_code == 200
    assert "top_products" in response.json()
    # You can add more specific checks depending on your test data


# Test the top_suppliers endpoint (GET /top_suppliers)
def test_top_suppliers():
    response = client.get("/top_suppliers?start_date=2025-01-01&end_date=2025-01-31")
    assert response.status_code == 200
    assert "top_suppliers" in response.json()


# Test creating a new order (POST /create_order)
def test_create_order():
    data = {
        "supplier_id": 1,
        "customer_id": 2,
        "quantity": 100,
        "price": 150.75,
        "order_date": "2025-01-15",
    }
    response = client.post("/create_order", json=data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Order added to queue"
    assert "order_id" in response.json()  # Ensure order_id is returned
