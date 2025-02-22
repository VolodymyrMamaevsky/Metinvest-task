import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.services.orders import (
    get_total_spent,
    get_top_products,
    get_top_suppliers,
    create_order,
)
from app.models.schemas import (
    OrderCreate,
    TotalSpentResponse,
    TopProductResponse,
    TopSupplierResponse,
)
from app.core.config import logger
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to get the total amount spent within a date range
@router.get("/total_spent", response_model=TotalSpentResponse)
async def total_spent(
    start_date: datetime, end_date: datetime, db: Session = Depends(get_db)
):
    start_time = time.time()
    logger.info(f"Request to get total spending from {start_date} to {end_date}")

    try:
        total = get_total_spent(db, start_date, end_date)
        if total is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data available for the specified period",
            )
        execution_time = time.time() - start_time
        logger.info(
            f"Response with total spending: {total}. Execution time: {execution_time:.4f} seconds."
        )
        return {"total_spent": total}
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(
            f"Error retrieving data: {e}. Execution time: {execution_time:.4f} seconds."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing request",
        )


# Endpoint to get the top 10 products within a date range
@router.get("/top_products", response_model=Dict[str, List[TopProductResponse]])
async def top_products(
    start_date: datetime, end_date: datetime, db: Session = Depends(get_db)
):
    start_time = time.time()
    logger.info(f"Request to get top 10 products from {start_date} to {end_date}")

    try:
        products = get_top_products(db, start_date, end_date)
        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data available for the specified period",
            )
        execution_time = time.time() - start_time
        logger.info(
            f"Response with top 10 products: {products}. Execution time: {execution_time:.4f} seconds."
        )
        return {
            "top_products": [{"product_id": p[0], "total_sold": p[1]} for p in products]
        }
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(
            f"Error retrieving data: {e}. Execution time: {execution_time:.4f} seconds."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing request",
        )


# Endpoint to get the top 5 suppliers within a date range
@router.get("/top_suppliers", response_model=Dict[str, List[TopSupplierResponse]])
async def top_suppliers(
    start_date: datetime, end_date: datetime, db: Session = Depends(get_db)
):
    start_time = time.time()
    logger.info(f"Request to get top 5 suppliers from {start_date} to {end_date}")

    try:
        suppliers = get_top_suppliers(db, start_date, end_date)
        if not suppliers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data available for the specified period",
            )
        execution_time = time.time() - start_time
        logger.info(
            f"Response with top 5 suppliers: {suppliers}. Execution time: {execution_time:.4f} seconds."
        )
        return {
            "top_suppliers": [
                {"supplier_id": s[0], "total_orders": s[1]} for s in suppliers
            ]
        }
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(
            f"Error retrieving data: {e}. Execution time: {execution_time:.4f} seconds."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing request",
        )


# Endpoint to create a new order
@router.post("/create_order")
async def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    order_id = create_order(db, order)
    return {"message": "Order added to queue", "order_id": order_id}
