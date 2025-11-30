"""Tests for filter functionality across all analytics types"""
import pytest
from datetime import datetime, timedelta


def test_sales_date_range_filter(client, sample_sales_data):
    """Test filtering sales by date range"""
    start_date = (datetime.now() - timedelta(days=10)).isoformat()
    end_date = (datetime.now() - timedelta(days=1)).isoformat()
    
    response = client.get(
        f"/api/v1/aggregate?analytics_type=sales&aggregation_type=count&field=amount"
        f"&start_date={start_date}&end_date={end_date}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "filters_applied" in data


def test_sales_multiple_filters(client, sample_sales_data):
    """Test combining multiple filters for sales"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount"
        "&category=Electronics&region=North"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] >= 0


def test_food_delivery_city_filter(client, sample_food_orders):
    """Test filtering food orders by city"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount&city=Mumbai"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] >= 0


def test_food_delivery_status_filter(client, sample_food_orders):
    """Test filtering food orders by delivery status"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=count&field=total_amount&delivery_status=delivered"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] >= 0


def test_saas_status_filter(client, sample_subscriptions):
    """Test filtering SaaS subscriptions by status"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr&status=active"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] >= 0


def test_saas_plan_filter(client, sample_subscriptions):
    """Test filtering SaaS subscriptions by plan"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=saas&aggregation_type=count&field=mrr&plan_name=Pro"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] >= 0
