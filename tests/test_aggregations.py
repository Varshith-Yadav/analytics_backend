"""Tests for aggregation endpoints"""
import pytest
from fastapi.testclient import TestClient


def test_sum_aggregation_basic(client, sample_sales_data):
    """Test basic sum aggregation without filters"""
    response = client.get("/api/v1/aggregate?aggregation_type=sum&field=amount")
    assert response.status_code == 200
    data = response.json()
    assert data["aggregation_type"] == "sum"
    assert data["field"] == "amount"
    assert data["value"] > 0
    assert isinstance(data["value"], float)


def test_avg_aggregation_with_filter(client, sample_sales_data):
    """Test average aggregation with category filter"""
    response = client.get(
        "/api/v1/aggregate?aggregation_type=avg&field=amount&category=Electronics"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["aggregation_type"] == "avg"
    assert data["field"] == "amount"
    assert data["value"] > 0
    assert "Electronics" in str(data["filters_applied"])


def test_count_aggregation_with_region_filter(client, sample_sales_data):
    """Test count aggregation with region filter"""
    response = client.get(
        "/api/v1/aggregate?aggregation_type=count&field=amount&region=North"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["aggregation_type"] == "count"
    assert data["value"] >= 0
    assert isinstance(data["value"], float)


def test_group_by_category(client, sample_sales_data):
    """Test aggregation with group_by parameter"""
    response = client.get(
        "/api/v1/aggregate?aggregation_type=sum&field=amount&group_by=category"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["aggregation_type"] == "sum"
    assert data["group_by"] == "category"
    assert "groups" in data
    assert isinstance(data["groups"], list)
    assert len(data["groups"]) > 0
    assert "group" in data["groups"][0]
    assert "value" in data["groups"][0]


def test_invalid_field_error(client, sample_sales_data):
    """Test error handling for invalid field"""
    response = client.get(
        "/api/v1/aggregate?aggregation_type=sum&field=invalid_field"
    )
    assert response.status_code == 400
    assert "error" in response.json() or "detail" in response.json()


def test_invalid_group_by_error(client, sample_sales_data):
    """Test error handling for invalid group_by field"""
    response = client.get(
        "/api/v1/aggregate?aggregation_type=sum&field=amount&group_by=invalid_field"
    )
    assert response.status_code == 400
    assert "error" in response.json() or "detail" in response.json()

