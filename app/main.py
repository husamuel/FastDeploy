# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="Product Registration API",
    description="Simple API for product registration and management",
    version="1.0.0"
)

# Pydantic models
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    category: str = Field(..., min_length=1, max_length=50, description="Product category")
    stock_quantity: int = Field(..., ge=0, description="Stock quantity")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    stock_quantity: Optional[int] = Field(None, ge=0)

class Product(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float
    category: str
    stock_quantity: int
    created_at: datetime
    updated_at: datetime

# In-memory storage (replace with database in production)
products_db = {}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Product Registration API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "products": "/products",
            "docs": "/docs"
        }
    }

# Get all products
@app.get("/products", response_model=List[Product])
async def get_products():
    return list(products_db.values())

# Get product by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return products_db[product_id]

# Create new product
@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate):
    product_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    product = Product(
        id=product_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        category=product_data.category,
        stock_quantity=product_data.stock_quantity,
        created_at=now,
        updated_at=now
    )
    
    products_db[product_id] = product
    return product

# Update product
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_data: ProductUpdate):
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    product = products_db[product_id]
    update_data = product_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    product.updated_at = datetime.utcnow()
    products_db[product_id] = product
    
    return product

# Delete product
@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    del products_db[product_id]
    return {"message": f"Product {product_id} deleted successfully"}

# Get products by category
@app.get("/products/category/{category}", response_model=List[Product])
async def get_products_by_category(category: str):
    filtered_products = [
        product for product in products_db.values() 
        if product.category.lower() == category.lower()
    ]
    return filtered_products

# Search products by name
@app.get("/products/search/{query}", response_model=List[Product])
async def search_products(query: str):
    filtered_products = [
        product for product in products_db.values() 
        if query.lower() in product.name.lower()
    ]
    return filtered_products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)