"""Tests for aggregation endpoints across all analytics types"""
import pytest
from fastapi.testclient import TestClient


def test_sales_sum_aggregation_basic(client, sample_sales_data):
    """Test basic sum aggregation for sales without filters"""
    response = client.get("/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "sales"
    assert data["aggregation_type"] == "sum"
    assert data["field"] == "amount"
    assert data["value"] > 0
    assert isinstance(data["value"], float)


def test_sales_avg_aggregation_with_filter(client, sample_sales_data):
    """Test average aggregation for sales with category filter"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=sales&aggregation_type=avg&field=amount&category=Electronics"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "sales"
    assert data["aggregation_type"] == "avg"
    assert data["field"] == "amount"
    assert data["value"] > 0


def test_sales_group_by_category(client, sample_sales_data):
    """Test sales aggregation with group_by parameter"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount&group_by=category"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "sales"
    assert data["aggregation_type"] == "sum"
    assert data["group_by"] == "category"
    assert "groups" in data
    assert isinstance(data["groups"], list)
    assert len(data["groups"]) > 0


def test_food_delivery_aggregation(client, sample_food_orders):
    """Test aggregation for food delivery analytics"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "food_delivery"
    assert data["aggregation_type"] == "sum"
    assert data["field"] == "total_amount"
    assert data["value"] > 0


def test_food_delivery_group_by_cuisine(client, sample_food_orders):
    """Test food delivery aggregation with grouping"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=food_delivery&aggregation_type=sum&field=total_amount&group_by=cuisine_type"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "food_delivery"
    assert "groups" in data
    assert len(data["groups"]) > 0


def test_saas_aggregation(client, sample_subscriptions):
    """Test aggregation for SaaS subscriptions"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "saas"
    assert data["aggregation_type"] == "sum"
    assert data["field"] == "mrr"
    assert data["value"] > 0


def test_saas_group_by_plan(client, sample_subscriptions):
    """Test SaaS aggregation with plan grouping"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=saas&aggregation_type=sum&field=mrr&group_by=plan_name"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "saas"
    assert "groups" in data


def test_invalid_field_error(client, sample_sales_data):
    """Test error handling for invalid field"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=invalid_field"
    )
    assert response.status_code == 400
    assert "detail" in response.json()


def test_invalid_group_by_error(client, sample_sales_data):
    """Test error handling for invalid group_by field"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=sales&aggregation_type=sum&field=amount&group_by=invalid_field"
    )
    assert response.status_code == 400
    assert "detail" in response.json()


def test_invalid_analytics_type(client):
    """Test error handling for invalid analytics type"""
    response = client.get(
        "/api/v1/aggregate?analytics_type=invalid&aggregation_type=sum&field=amount"
    )
    assert response.status_code == 422  # Validation error
