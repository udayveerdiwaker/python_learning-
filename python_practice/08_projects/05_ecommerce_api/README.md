# Project 05: E-Commerce API Micro-Service

This project implements a product catalog, guest shopping carts tracked by session identifiers, and transactional checkouts that validate product stock levels.

---

## 🚀 How to Run Locally

1. Navigate to this folder:
   ```bash
   cd python_practice/08_projects/05_ecommerce_api
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. Open your browser and navigate to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📮 Postman API Request Guides

### 1. View Products (GET `/products`)
- **URL:** `http://127.0.0.1:8000/products`
- **Method:** `GET`
- *(Returns list of keyboard, mouse, USB hubs, webcams, and their stock counts).*

### 2. Add Item to Cart (POST `/cart`)
- **URL:** `http://127.0.0.1:8000/cart?session_id=guest_session_123`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "product_id": 1,
    "quantity": 2
  }
  ```

### 3. View Session Cart (GET `/cart`)
- **URL:** `http://127.0.0.1:8000/cart?session_id=guest_session_123`
- **Method:** `GET`

### 4. Checkout Cart (POST `/checkout`)
- **URL:** `http://127.0.0.1:8000/checkout`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "session_id": "guest_session_123",
    "customer_email": "customer@example.com"
  }
  ```
- *(If successful, returns a created invoice showing line item prices and total amounts. Product stock levels are reduced. Repeating this request will fail since the cart is cleared).*
