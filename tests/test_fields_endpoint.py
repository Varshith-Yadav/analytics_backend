"""Tests for fields endpoint"""
import pytest


def test_fields_endpoint_sales(client):
    """Test fields endpoint for sales analytics"""
    response = client.get("/api/v1/fields?analytics_type=sales")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "sales"
    assert "aggregatable_fields" in data
    assert "groupable_fields" in data
    assert "filterable_fields" in data
    assert "amount" in data["aggregatable_fields"]
    assert "quantity" in data["aggregatable_fields"]


def test_fields_endpoint_food_delivery(client):
    """Test fields endpoint for food delivery analytics"""
    response = client.get("/api/v1/fields?analytics_type=food_delivery")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "food_delivery"
    assert "total_amount" in data["aggregatable_fields"]
    assert "cuisine_type" in data["groupable_fields"]


def test_fields_endpoint_saas(client):
    """Test fields endpoint for SaaS analytics"""
    response = client.get("/api/v1/fields?analytics_type=saas")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "saas"
    assert "mrr" in data["aggregatable_fields"]
    assert "plan_name" in data["groupable_fields"]

