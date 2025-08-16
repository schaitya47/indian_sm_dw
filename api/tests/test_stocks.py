"""
Test stock API endpoints.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.models import DimStock


def test_list_stocks_empty(client: TestClient):
    """Test listing stocks when database is empty."""
    response = client.get("/api/v1/stocks")
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "meta" in data
    assert len(data["data"]) == 0


def test_search_stocks_empty(client: TestClient):
    """Test searching stocks when database is empty."""
    response = client.get("/api/v1/stocks/search?q=TCS")
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 0


def test_list_industries_empty(client: TestClient):
    """Test listing industries when database is empty."""
    response = client.get("/api/v1/stocks/industries")
    assert response.status_code == 200
    
    data = response.json()
    assert "industries" in data
    assert len(data["industries"]) == 0


def test_get_stock_not_found(client: TestClient):
    """Test getting a stock that doesn't exist."""
    response = client.get("/api/v1/stocks/NONEXISTENT")
    assert response.status_code == 404


def test_stock_endpoints_with_data(client: TestClient, db: Session):
    """Test stock endpoints with sample data."""
    # Create sample stock
    stock = DimStock(
        nk_symbol="TCS",
        company_name="Tata Consultancy Services",
        industry="Information Technology",
        series="EQ",
        isin_code="INE467B01029"
    )
    db.add(stock)
    db.commit()
    
    # Test list stocks
    response = client.get("/api/v1/stocks")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["symbol"] == "TCS"
    
    # Test search stocks
    response = client.get("/api/v1/stocks/search?q=TCS")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["symbol"] == "TCS"
    
    # Test get stock by symbol
    response = client.get("/api/v1/stocks/TCS")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TCS"
    assert data["company_name"] == "Tata Consultancy Services"
    
    # Test industries
    response = client.get("/api/v1/stocks/industries")
    assert response.status_code == 200
    data = response.json()
    assert "Information Technology" in data["industries"]
