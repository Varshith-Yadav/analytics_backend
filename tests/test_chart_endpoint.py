"""Tests for chart-ready JSON endpoint across all analytics types"""
import pytest


def test_sales_chart_data_basic(client, sample_sales_data):
    """Test basic chart data retrieval for sales"""
    response = client.get(
        "/api/v1/chart?analytics_type=sales&chart_type=bar&field=amount&group_by=category"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "sales"
    assert data["chart_type"] == "bar"
    assert "data" in data
    assert isinstance(data["data"], list)


def test_food_delivery_chart_data(client, sample_food_orders):
    """Test chart data for food delivery"""
    response = client.get(
        "/api/v1/chart?analytics_type=food_delivery&chart_type=pie&field=total_amount&group_by=cuisine_type"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "food_delivery"
    assert data["chart_type"] == "pie"
    assert "data" in data


def test_saas_chart_data(client, sample_subscriptions):
    """Test chart data for SaaS subscriptions"""
    response = client.get(
        "/api/v1/chart?analytics_type=saas&chart_type=bar&field=mrr&group_by=plan_name"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analytics_type"] == "saas"
    assert "data" in data
