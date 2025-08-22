import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_products_db():
    """Clear the in-memory database before each test"""
    from main import products_db
    products_db.clear()
    yield
    products_db.clear()

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product Registration API"
    assert data["version"] == "1.0.0"

def test_get_empty_products():
    """Test getting products when database is empty"""
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product():
    """Test creating a new product"""
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "category": "Electronics",
        "stock_quantity": 10
    }
    
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["category"] == product_data["category"]
    assert "id" in data
    assert "created_at" in data

def test_create_product_invalid_price():
    """Test creating a product with invalid price"""
    product_data = {
        "name": "Test Product",
        "price": -10.0,  # Invalid negative price
        "category": "Electronics",
        "stock_quantity": 10
    }
    
    response = client.post("/products", json=product_data)
    assert response.status_code == 422

def test_get_product_by_id():
    """Test getting a specific product by ID"""
    # First create a product
    product_data = {
        "name": "Test Product",
        "price": 50.0,
        "category": "Books",
        "stock_quantity": 5
    }
    
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]
    
    # Then get it by ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]

def test_get_nonexistent_product():
    """Test getting a product that doesn't exist"""
    response = client.get("/products/nonexistent-id")
    assert response.status_code == 404

def test_update_product():
    """Test updating a product"""
    # Create a product first
    product_data = {
        "name": "Original Product",
        "price": 100.0,
        "category": "Electronics",
        "stock_quantity": 10
    }
    
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]
    
    # Update the product
    update_data = {
        "name": "Updated Product",
        "price": 150.0
    }
    
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]
    assert data["category"] == product_data["category"]  # Should remain unchanged

def test_delete_product():
    """Test deleting a product"""
    # Create a product first
    product_data = {
        "name": "Product to Delete",
        "price": 25.0,
        "category": "Test",
        "stock_quantity": 1
    }
    
    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]
    
    # Delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_get_products_by_category():
    """Test getting products by category"""
    # Create products in different categories
    products = [
        {"name": "Laptop", "price": 1000, "category": "Electronics", "stock_quantity": 5},
        {"name": "Book", "price": 20, "category": "Books", "stock_quantity": 10},
        {"name": "Phone", "price": 500, "category": "Electronics", "stock_quantity": 3}
    ]
    
    for product in products:
        client.post("/products", json=product)
    
    # Get electronics products
    response = client.get("/products/category/Electronics")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    for product in data:
        assert product["category"] == "Electronics"

def test_search_products():
    """Test searching products by name"""
    # Create test products
    products = [
        {"name": "Gaming Laptop", "price": 1500, "category": "Electronics", "stock_quantity": 2},
        {"name": "Office Laptop", "price": 800, "category": "Electronics", "stock_quantity": 5},
        {"name": "Gaming Mouse", "price": 50, "category": "Accessories", "stock_quantity": 10}
    ]
    
    for product in products:
        client.post("/products", json=product)
    
    # Search for "laptop"
    response = client.get("/products/search/laptop")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    for product in data:
        assert "laptop" in product["name"].lower()