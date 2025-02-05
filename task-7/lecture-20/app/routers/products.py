from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db, Product as ProductModel

router = APIRouter()

class Product(BaseModel):
    name: str
    price: float

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(ProductModel).all()
        response = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving products")

@router.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    try:
        db_product = ProductModel(name=product.name, price=product.price)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return {"message": "Product added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding the product")