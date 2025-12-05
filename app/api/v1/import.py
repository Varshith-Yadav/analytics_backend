"""Data import API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.utils.data_import import DataImporter
import tempfile
import os

router = APIRouter(prefix="/api/v1/import", tags=["Data Import"])


@router.post("/sales/csv")
async def import_sales_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Import sales transactions from CSV file.
    
    Expected CSV columns:
    product_name, category, amount, quantity, region, customer_id (optional),
    payment_method (optional), sale_date
    """
    tmp_file_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Import data
        count = DataImporter.import_sales_from_csv(tmp_file_path, db)
        
        # Clean up
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "analytics_type": "sales",
            "records_imported": count,
            "message": f"Successfully imported {count} sales transactions"
        }
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")


@router.post("/sales/json")
async def import_sales_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import sales transactions from JSON file"""
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        count = DataImporter.import_sales_from_json(tmp_file_path, db)
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "analytics_type": "sales",
            "records_imported": count,
            "message": f"Successfully imported {count} sales transactions"
        }
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")


@router.post("/food_delivery/csv")
async def import_food_orders_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import food delivery orders from CSV file"""
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        count = DataImporter.import_food_orders_from_csv(tmp_file_path, db)
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "analytics_type": "food_delivery",
            "records_imported": count,
            "message": f"Successfully imported {count} food orders"
        }
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")


@router.post("/food_delivery/json")
async def import_food_orders_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import food delivery orders from JSON file"""
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        count = DataImporter.import_food_orders_from_json(tmp_file_path, db)
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "analytics_type": "food_delivery",
            "records_imported": count,
            "message": f"Successfully imported {count} food orders"
        }
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")


@router.post("/saas/csv")
async def import_subscriptions_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import SaaS subscriptions from CSV file"""
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        count = DataImporter.import_subscriptions_from_csv(tmp_file_path, db)
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "analytics_type": "saas",
            "records_imported": count,
            "message": f"Successfully imported {count} subscriptions"
        }
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")


@router.post("/saas/json")
async def import_subscriptions_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import SaaS subscriptions from JSON file"""
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        count = DataImporter.import_subscriptions_from_json(tmp_file_path, db)
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "analytics_type": "saas",
            "records_imported": count,
            "message": f"Successfully imported {count} subscriptions"
        }
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=400, detail=f"Error importing data: {str(e)}")

