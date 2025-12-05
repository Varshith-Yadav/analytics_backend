"""
Data import utilities for organizations to load their own datasets
Supports CSV and JSON import for all three analytics types
"""
import csv
import json
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import SalesTransaction, FoodOrder, Subscription
from app.core.database import SessionLocal
import uuid


class DataImporter:
    """Utility class for importing data from CSV/JSON files"""

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse date string in various formats"""
        if isinstance(date_str, datetime):
            return date_str
        
        # Try common date formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")

    @staticmethod
    def import_sales_from_csv(file_path: str, db: Optional[Session] = None) -> int:
        """
        Import sales transactions from CSV file.
        
        Expected CSV columns:
        - product_name, category, amount, quantity, region, customer_id (optional), 
          payment_method (optional), sale_date
        
        Returns: Number of records imported
        """
        if db is None:
            db = SessionLocal()
        
        try:
            transactions = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    transaction = SalesTransaction(
                        product_name=row.get('product_name', '').strip(),
                        category=row.get('category', '').strip(),
                        amount=float(row.get('amount', 0)),
                        quantity=int(row.get('quantity', 1)),
                        region=row.get('region', '').strip(),
                        customer_id=row.get('customer_id', f"CUST_{uuid.uuid4().hex[:8]}"),
                        payment_method=row.get('payment_method', 'credit_card'),
                        sale_date=DataImporter.parse_date(row.get('sale_date', datetime.now().isoformat()))
                    )
                    transactions.append(transaction)
            
            db.bulk_save_objects(transactions)
            db.commit()
            print(f"✓ Imported {len(transactions)} sales transactions from {file_path}")
            return len(transactions)
        except Exception as e:
            db.rollback()
            print(f"✗ Error importing sales data: {e}")
            raise
        finally:
            if db is not None:
                db.close()

    @staticmethod
    def import_sales_from_json(file_path: str, db: Optional[Session] = None) -> int:
        """
        Import sales transactions from JSON file.
        
        Expected JSON format:
        [
            {
                "product_name": "...",
                "category": "...",
                "amount": 100.0,
                "quantity": 2,
                "region": "...",
                "customer_id": "...",
                "payment_method": "...",
                "sale_date": "2024-01-01T00:00:00"
            }
        ]
        """
        if db is None:
            db = SessionLocal()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            transactions = []
            for item in data:
                transaction = SalesTransaction(
                    product_name=item.get('product_name', ''),
                    category=item.get('category', ''),
                    amount=float(item.get('amount', 0)),
                    quantity=int(item.get('quantity', 1)),
                    region=item.get('region', ''),
                    customer_id=item.get('customer_id', f"CUST_{uuid.uuid4().hex[:8]}"),
                    payment_method=item.get('payment_method', 'credit_card'),
                    sale_date=DataImporter.parse_date(item.get('sale_date', datetime.now().isoformat()))
                )
                transactions.append(transaction)
            
            db.bulk_save_objects(transactions)
            db.commit()
            print(f"✓ Imported {len(transactions)} sales transactions from {file_path}")
            return len(transactions)
        except Exception as e:
            db.rollback()
            print(f"✗ Error importing sales data: {e}")
            raise
        finally:
            if db is not None:
                db.close()

    @staticmethod
    def import_food_orders_from_csv(file_path: str, db: Optional[Session] = None) -> int:
        """
        Import food delivery orders from CSV file.
        
        Expected CSV columns:
        - order_id, restaurant_name, cuisine_type, order_amount, delivery_fee, 
          tip_amount, total_amount, customer_id (optional), city, delivery_status,
          order_date, delivery_time_minutes (optional)
        
        Note: Duplicate order_id values will be skipped.
        """
        if db is None:
            db = SessionLocal()
        
        try:
            orders = []
            skipped = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    order_id = row.get('order_id', f"ORD_{uuid.uuid4().hex[:8].upper()}").strip()
                    
                    # Check if order_id already exists
                    existing = db.query(FoodOrder).filter(FoodOrder.order_id == order_id).first()
                    if existing:
                        skipped += 1
                        continue
                    
                    order = FoodOrder(
                        order_id=order_id,
                        restaurant_name=row.get('restaurant_name', '').strip(),
                        cuisine_type=row.get('cuisine_type', '').strip(),
                        order_amount=float(row.get('order_amount', 0)),
                        delivery_fee=float(row.get('delivery_fee', 0)),
                        tip_amount=float(row.get('tip_amount', 0)),
                        total_amount=float(row.get('total_amount', 0)),
                        customer_id=row.get('customer_id', f"CUST_{uuid.uuid4().hex[:8]}"),
                        city=row.get('city', '').strip(),
                        delivery_status=row.get('delivery_status', 'pending'),
                        order_date=DataImporter.parse_date(row.get('order_date', datetime.now().isoformat())),
                        delivery_time_minutes=int(row.get('delivery_time_minutes', 0)) if row.get('delivery_time_minutes') else None
                    )
                    orders.append(order)
            
            if orders:
                db.bulk_save_objects(orders)
                db.commit()
            
            if skipped > 0:
                print(f"✓ Imported {len(orders)} food orders from {file_path} (skipped {skipped} duplicates)")
            else:
                print(f"✓ Imported {len(orders)} food orders from {file_path}")
            return len(orders)
        except Exception as e:
            db.rollback()
            print(f"✗ Error importing food orders: {e}")
            raise
        finally:
            if db is not None:
                db.close()

    @staticmethod
    def import_food_orders_from_json(file_path: str, db: Optional[Session] = None) -> int:
        """
        Import food delivery orders from JSON file.
        
        Note: Duplicate order_id values will be skipped.
        """
        if db is None:
            db = SessionLocal()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            orders = []
            skipped = 0
            for item in data:
                order_id = item.get('order_id', f"ORD_{uuid.uuid4().hex[:8].upper()}")
                
                # Check if order_id already exists
                existing = db.query(FoodOrder).filter(FoodOrder.order_id == order_id).first()
                if existing:
                    skipped += 1
                    continue
                
                order = FoodOrder(
                    order_id=order_id,
                    restaurant_name=item.get('restaurant_name', ''),
                    cuisine_type=item.get('cuisine_type', ''),
                    order_amount=float(item.get('order_amount', 0)),
                    delivery_fee=float(item.get('delivery_fee', 0)),
                    tip_amount=float(item.get('tip_amount', 0)),
                    total_amount=float(item.get('total_amount', 0)),
                    customer_id=item.get('customer_id', f"CUST_{uuid.uuid4().hex[:8]}"),
                    city=item.get('city', ''),
                    delivery_status=item.get('delivery_status', 'pending'),
                    order_date=DataImporter.parse_date(item.get('order_date', datetime.now().isoformat())),
                    delivery_time_minutes=int(item.get('delivery_time_minutes', 0)) if item.get('delivery_time_minutes') else None
                )
                orders.append(order)
            
            if orders:
                db.bulk_save_objects(orders)
                db.commit()
            
            if skipped > 0:
                print(f"✓ Imported {len(orders)} food orders from {file_path} (skipped {skipped} duplicates)")
            else:
                print(f"✓ Imported {len(orders)} food orders from {file_path}")
            return len(orders)
        except Exception as e:
            db.rollback()
            print(f"✗ Error importing food orders: {e}")
            raise
        finally:
            if db is not None:
                db.close()

    @staticmethod
    def import_subscriptions_from_csv(file_path: str, db: Optional[Session] = None) -> int:
        """
        Import SaaS subscriptions from CSV file.
        
        Expected CSV columns:
        - subscription_id, customer_id, plan_name, plan_type, amount, status,
          currency, billing_cycle_start, billing_cycle_end, cancelled_at (optional), mrr
        
        Note: Duplicate subscription_id values will be skipped.
        """
        if db is None:
            db = SessionLocal()
        
        try:
            subscriptions = []
            skipped = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    subscription_id = row.get('subscription_id', f"SUB_{uuid.uuid4().hex[:8].upper()}").strip()
                    
                    # Check if subscription_id already exists
                    existing = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
                    if existing:
                        skipped += 1
                        continue
                    
                    billing_start = DataImporter.parse_date(row.get('billing_cycle_start', datetime.now().isoformat()))
                    billing_end = DataImporter.parse_date(row.get('billing_cycle_end', datetime.now().isoformat()))
                    
                    subscription = Subscription(
                        subscription_id=subscription_id,
                        customer_id=row.get('customer_id', f"CUST_{uuid.uuid4().hex[:8]}"),
                        plan_name=row.get('plan_name', '').strip(),
                        plan_type=row.get('plan_type', 'monthly'),
                        amount=float(row.get('amount', 0)),
                        status=row.get('status', 'active'),
                        currency=row.get('currency', 'USD'),
                        billing_cycle_start=billing_start,
                        billing_cycle_end=billing_end,
                        cancelled_at=DataImporter.parse_date(row['cancelled_at']) if row.get('cancelled_at') else None,
                        mrr=float(row.get('mrr', 0))
                    )
                    subscriptions.append(subscription)
            
            if subscriptions:
                db.bulk_save_objects(subscriptions)
                db.commit()
            
            if skipped > 0:
                print(f"✓ Imported {len(subscriptions)} subscriptions from {file_path} (skipped {skipped} duplicates)")
            else:
                print(f"✓ Imported {len(subscriptions)} subscriptions from {file_path}")
            return len(subscriptions)
        except Exception as e:
            db.rollback()
            print(f"✗ Error importing subscriptions: {e}")
            raise
        finally:
            if db is not None:
                db.close()

    @staticmethod
    def import_subscriptions_from_json(file_path: str, db: Optional[Session] = None) -> int:
        """
        Import SaaS subscriptions from JSON file.
        
        Note: Duplicate subscription_id values will be skipped.
        """
        if db is None:
            db = SessionLocal()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            subscriptions = []
            skipped = 0
            for item in data:
                subscription_id = item.get('subscription_id', f"SUB_{uuid.uuid4().hex[:8].upper()}")
                
                # Check if subscription_id already exists
                existing = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
                if existing:
                    skipped += 1
                    continue
                
                billing_start = DataImporter.parse_date(item.get('billing_cycle_start', datetime.now().isoformat()))
                billing_end = DataImporter.parse_date(item.get('billing_cycle_end', datetime.now().isoformat()))
                
                subscription = Subscription(
                    subscription_id=subscription_id,
                    customer_id=item.get('customer_id', f"CUST_{uuid.uuid4().hex[:8]}"),
                    plan_name=item.get('plan_name', ''),
                    plan_type=item.get('plan_type', 'monthly'),
                    amount=float(item.get('amount', 0)),
                    status=item.get('status', 'active'),
                    currency=item.get('currency', 'USD'),
                    billing_cycle_start=billing_start,
                    billing_cycle_end=billing_end,
                    cancelled_at=DataImporter.parse_date(item['cancelled_at']) if item.get('cancelled_at') else None,
                    mrr=float(item.get('mrr', 0))
                )
                subscriptions.append(subscription)
            
            if subscriptions:
                db.bulk_save_objects(subscriptions)
                db.commit()
            
            if skipped > 0:
                print(f"✓ Imported {len(subscriptions)} subscriptions from {file_path} (skipped {skipped} duplicates)")
            else:
                print(f"✓ Imported {len(subscriptions)} subscriptions from {file_path}")
            return len(subscriptions)
        except Exception as e:
            db.rollback()
            print(f"✗ Error importing subscriptions: {e}")
            raise
        finally:
            if db is not None:
                db.close()


def import_data_cli():
    """CLI interface for data import"""
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python -m app.utils.data_import <analytics_type> <file_path> <format>")
        print("  analytics_type: sales | food_delivery | saas")
        print("  file_path: Path to CSV or JSON file")
        print("  format: csv | json")
        sys.exit(1)
    
    analytics_type = sys.argv[1].lower()
    file_path = sys.argv[2]
    file_format = sys.argv[3].lower()
    
    if analytics_type == "sales":
        if file_format == "csv":
            DataImporter.import_sales_from_csv(file_path)
        elif file_format == "json":
            DataImporter.import_sales_from_json(file_path)
        else:
            print("Invalid format. Use 'csv' or 'json'")
    
    elif analytics_type == "food_delivery":
        if file_format == "csv":
            DataImporter.import_food_orders_from_csv(file_path)
        elif file_format == "json":
            DataImporter.import_food_orders_from_json(file_path)
        else:
            print("Invalid format. Use 'csv' or 'json'")
    
    elif analytics_type == "saas":
        if file_format == "csv":
            DataImporter.import_subscriptions_from_csv(file_path)
        elif file_format == "json":
            DataImporter.import_subscriptions_from_json(file_path)
        else:
            print("Invalid format. Use 'csv' or 'json'")
    
    else:
        print("Invalid analytics_type. Use 'sales', 'food_delivery', or 'saas'")


if __name__ == "__main__":
    import_data_cli()

