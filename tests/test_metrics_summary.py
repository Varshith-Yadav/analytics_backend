"""Tests for metrics summary endpoint across all analytics types"""
import pytest


def test_sales_metrics_summary(client, sample_sales_data):
    """Test metrics summary for sales"""
    response = client.get("/api/v1/metrics/summary?analytics_type=sales")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "sales"
    assert "total" in data
    assert "average" in data
    assert "count" in data


def test_food_delivery_metrics_summary(client, sample_food_orders):
    """Test metrics summary for food delivery"""
    response = client.get("/api/v1/metrics/summary?analytics_type=food_delivery")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "food_delivery"
    assert "total" in data
    assert "average" in data
    assert "count" in data


def test_saas_metrics_summary(client, sample_subscriptions):
    """Test metrics summary for SaaS"""
    response = client.get("/api/v1/metrics/summary?analytics_type=saas")
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "saas"
    assert "total" in data
    assert "average" in data
    assert "count" in data
