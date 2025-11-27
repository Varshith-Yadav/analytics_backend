"""
Sample client to demonstrate API usage
This script shows how to interact with the Analytics Backend API
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


def test_aggregations():
    """Test various aggregation endpoints"""
    print("\n" + "="*60)
    print("TESTING AGGREGATIONS")
    print("="*60)

    # 1. Sum aggregation
    print("\n1. Sum of all sales amounts:")
    response = requests.get(f"{BASE_URL}/api/v1/aggregate?aggregation_type=sum&field=amount")
    print_response("Sum Aggregation", response.json())

    # 2. Average with filter
    print("\n2. Average transaction amount for Electronics:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?aggregation_type=avg&field=amount&category=Electronics"
    )
    print_response("Average with Filter", response.json())

    # 3. Count by region
    print("\n3. Transaction count grouped by region:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?aggregation_type=count&field=amount&group_by=region"
    )
    print_response("Count by Region", response.json())

    # 4. Sum grouped by category
    print("\n4. Total sales grouped by category:")
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?aggregation_type=sum&field=amount&group_by=category"
    )
    print_response("Sum by Category", response.json())

    # 5. Date range filter
    print("\n5. Sales in last 30 days:")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?aggregation_type=sum&field=amount"
        f"&start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
    )
    print_response("Date Range Filter", response.json())


def test_chart_data():
    """Test chart-ready JSON endpoint"""
    print("\n" + "="*60)
    print("TESTING CHART DATA")
    print("="*60)

    # Bar chart by category
    print("\n1. Bar chart data - Sales by category:")
    response = requests.get(
        f"{BASE_URL}/api/v1/chart?chart_type=bar&field=amount&group_by=category"
    )
    print_response("Bar Chart Data", response.json())

    # Pie chart by region
    print("\n2. Pie chart data - Sales by region:")
    response = requests.get(
        f"{BASE_URL}/api/v1/chart?chart_type=pie&field=amount&group_by=region"
    )
    print_response("Pie Chart Data", response.json())

    # Line chart with filters
    print("\n3. Line chart data - Electronics sales by region:")
    response = requests.get(
        f"{BASE_URL}/api/v1/chart?chart_type=line&field=amount&group_by=region&category=Electronics"
    )
    print_response("Line Chart with Filters", response.json())


def test_metrics_summary():
    """Test metrics summary endpoint"""
    print("\n" + "="*60)
    print("TESTING METRICS SUMMARY")
    print("="*60)

    # Overall summary
    print("\n1. Overall metrics summary:")
    response = requests.get(f"{BASE_URL}/api/v1/metrics/summary")
    print_response("Overall Summary", response.json())

    # Filtered summary
    print("\n2. Filtered summary (Electronics, North region):")
    response = requests.get(
        f"{BASE_URL}/api/v1/metrics/summary?category=Electronics&region=North"
    )
    print_response("Filtered Summary", response.json())


def test_performance():
    """Test query performance"""
    print("\n" + "="*60)
    print("TESTING PERFORMANCE")
    print("="*60)

    # Measure query time
    start_time = time.time()
    response = requests.get(
        f"{BASE_URL}/api/v1/aggregate?aggregation_type=sum&field=amount&group_by=category"
    )
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    print(f"\nQuery execution time: {elapsed_time:.2f}ms")
    print(f"Target: <100ms")
    print(f"Status: {'✓ PASS' if elapsed_time < 100 else '✗ FAIL'}")
    print_response("Performance Test Result", response.json())


def main():
    """Run all client tests"""
    print("\n" + "="*60)
    print("ANALYTICS BACKEND - SAMPLE CLIENT")
    print("="*60)
    print("\nMake sure the server is running on http://localhost:8000")
    print("Start the server with: uvicorn app.main:app --reload\n")

    try:
        # Test health
        test_health_check()

        # Test aggregations
        test_aggregations()

        # Test chart data
        test_chart_data()

        # Test metrics summary
        test_metrics_summary()

        # Test performance
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

