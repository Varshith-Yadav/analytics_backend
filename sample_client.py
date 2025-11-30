"""
Sample client to demonstrate API usage for all three analytics domains
This script shows how to interact with Sales, Food Delivery, and SaaS analytics
"""
import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2, default=str))
    print(f"{'='*60}\n")


def test_health_check():
    """Test health endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response.json())


def test_available_fields():
    """Test available fields endpoint"""
    print("\n" + "="*60)
    print("TESTING AVAILABLE FIELDS")
    print("="*60)

    for analytics_type in ["sales", "food_delivery", "saas"]:
        print(f"\n{analytics_type.upper()} Fields:")
        response = requests.get(f"{BASE_URL}/api/v1/fields?analytics_type={analytics_type}")
        print_response(f"{analytics_type.title()} Available Fields", response.json())


def test_sales_analytics():
    """Test Sales/E-commerce Analytics"""
    print("\n" + "="*60)
    print("TESTING SALES / E-COMMERCE ANALYTICS")
    print("="*60)

    # 1. Total sales amount
    print("\n1. Total sales amount:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount"
    )
    print_response("Total Sales", response.json())

    # 2. Sales by category
    print("\n2. Sales grouped by category:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount&group_by=category"
    )
    print_response("Sales by Category", response.json())

    # 3. Average transaction with filter
    print("\n3. Average transaction amount for Electronics:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=sales&aggregation_type=avg&field=amount&category=Electronics"
    )
    print_response("Average Electronics Sale", response.json())

    # 4. Chart data - Sales by region
    print("\n4. Chart data - Sales by region:")
    response = requests.get(
        f"{BASE_URL}/api/v1/chart?analytics_type=sales&chart_type=bar&field=amount&group_by=region"
    )
    print_response("Sales by Region Chart", response.json())


def test_food_delivery_analytics():
    """Test Food Delivery Analytics"""
    print("\n" + "="*60)
    print("TESTING FOOD DELIVERY ANALYTICS (Swiggy/Zomato style)")
    print("="*60)

    # 1. Total order value
    print("\n1. Total order value:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount"
    )
    print_response("Total Order Value", response.json())

    # 2. Orders by cuisine type
    print("\n2. Orders grouped by cuisine type:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount&group_by=cuisine_type"
    )
    print_response("Orders by Cuisine", response.json())

    # 3. Average delivery time
    print("\n3. Average delivery time (minutes):")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=avg&field=delivery_time_minutes&delivery_status=delivered"
    )
    print_response("Average Delivery Time", response.json())

    # 4. Orders by city
    print("\n4. Orders by city:")
    response = requests.get(
        f"{BASE_URL}/api/v1/chart?analytics_type=food_delivery&chart_type=pie&field=total_amount&group_by=city"
    )
    print_response("Orders by City Chart", response.json())

    # 5. Delivery status breakdown
    print("\n5. Delivery status breakdown:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=count&field=total_amount&group_by=delivery_status"
    )
    print_response("Delivery Status Breakdown", response.json())


def test_saas_analytics():
    """Test SaaS Subscription Analytics"""
    print("\n" + "="*60)
    print("TESTING SAAS SUBSCRIPTION ANALYTICS (Stripe style)")
    print("="*60)

    # 1. Total MRR (Monthly Recurring Revenue)
    print("\n1. Total MRR (Monthly Recurring Revenue):")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr"
    )
    print_response("Total MRR", response.json())

    # 2. MRR by plan
    print("\n2. MRR grouped by plan:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr&group_by=plan_name"
    )
    print_response("MRR by Plan", response.json())

    # 3. Active subscriptions count
    print("\n3. Active subscriptions count:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=saas&aggregation_type=count&field=mrr&status=active"
    )
    print_response("Active Subscriptions", response.json())

    # 4. MRR by subscription status
    print("\n4. MRR by subscription status:")
    response = requests.get(
        f"{BASE_URL}/api/v1/chart?analytics_type=saas&chart_type=bar&field=mrr&group_by=status"
    )
    print_response("MRR by Status Chart", response.json())

    # 5. Average subscription value
    print("\n5. Average subscription amount:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?analytics_type=saas&aggregation_type=avg&field=amount&status=active"
    )
    print_response("Average Subscription Value", response.json())


def test_metrics_summary():
    """Test metrics summary for all analytics types"""
    print("\n" + "="*60)
    print("TESTING METRICS SUMMARY")
    print("="*60)

    for analytics_type in ["sales", "food_delivery", "saas"]:
        print(f"\n{analytics_type.upper()} Summary:")
        response = requests.get(f"{BASE_URL}/api/v1/metrics/summary?analytics_type={analytics_type}")
        print_response(f"{analytics_type.title()} Summary", response.json())


def test_performance():
    """Test query performance"""
    print("\n" + "="*60)
    print("TESTING PERFORMANCE")
    print("="*60)

    # Measure query time for each analytics type
    analytics_types = [
        ("sales", "amount", "category"),
        ("food_delivery", "total_amount", "cuisine_type"),
        ("saas", "mrr", "plan_name")
    ]

    for analytics_type, field, group_by in analytics_types:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}/api/v1/aggregate?analytics_type={analytics_type}&aggregation_type=sum&field={field}&group_by={group_by}"
        )
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        print(f"\n{analytics_type.upper()} Query:")
        print(f"  Execution time: {elapsed_time:.2f}ms")
        print(f"  Target: <100ms")
        print(f"  Status: {'✓ PASS' if elapsed_time < 100 else '✗ FAIL'}")
        assert response.status_code == 200


def main():
    """Run all client tests"""
    print("\n" + "="*60)
    print("MULTI-DOMAIN ANALYTICS BACKEND - SAMPLE CLIENT")
    print("="*60)
    print("\nMake sure the server is running on http://localhost:8000")
    print("Start the server with: uvicorn app.main:app --reload\n")

    try:
        # Test health
        test_health_check()

        # Test available fields
        test_available_fields()

        # Test Sales Analytics
        test_sales_analytics()

        # Test Food Delivery Analytics
        test_food_delivery_analytics()

        # Test SaaS Analytics
        test_saas_analytics()

        # Test Metrics Summary
        test_metrics_summary()

        # Test Performance
        test_performance()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to the server.")
        print("Please make sure the server is running on http://localhost:8000")
        print("Start it with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")


if __name__ == "__main__":
    main()
