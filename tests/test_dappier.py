import os
import pytest
from unittest.mock import patch
from dappier import Dappier

# Test Dappier initialization
def test_dappier_init_with_api_key():
    api_key = "test_api_key"
    dappier = Dappier(api_key=api_key)
    assert dappier.api_key == api_key
    assert dappier._headers["Authorization"] == f"Bearer {api_key}"
    assert dappier._headers["Content-Type"] == "application/json"

def test_dappier_init_with_env_variable(monkeypatch):
    api_key = "env_api_key"
    monkeypatch.setenv("DAPPIER_API_KEY", api_key)
    dappier = Dappier()
    assert dappier.api_key == api_key
    assert dappier._headers["Authorization"] == f"Bearer {api_key}"

def test_dappier_init_no_api_key():
    with pytest.raises(ValueError, match="API key must be provided either as an argument or through the environment variable DAPPIER_API_KEY."):
        Dappier()

# Test Dappier API methods
@patch("dappier.api.ai_models.requests.post")
def test_real_time_search_api(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "Success"}

    dappier = Dappier(api_key="test_api_key")
    query = "real-time data"
    response = dappier.real_time_search_api(query=query)

    mock_post.assert_called_once_with(
        "https://api.dappier.com/app/aimodel/am_01j06ytn18ejftedz6dyhz2b15",  # Replace BASE_URL with its actual value
        headers={"Authorization": "Bearer test_api_key", "Content-Type": "application/json"},
        data='{"query": "real-time data"}'
    )
    assert response.message == "Success"

@patch("dappier.api.ai_models.requests.post")
def test_polygon_stock_market_search_api(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "Stock Market Success"}

    dappier = Dappier(api_key="test_api_key")
    query = "stock market data"
    response = dappier.polygon_stock_market_search_api(query=query)

    mock_post.assert_called_once_with(
        "https://api.dappier.com/app/aimodel/am_01j749h8pbf7ns8r1bq9s2evrh",  # Replace BASE_URL with its actual value
        headers={"Authorization": "Bearer test_api_key", "Content-Type": "application/json"},
        data='{"query": "stock market data"}'
    )
    assert response.message == "Stock Market Success"

# Test Dappier representation
def test_dappier_repr():
    api_key = "test_api_key"
    dappier = Dappier(api_key=api_key)
    assert repr(dappier) == "Dappier(api_key=test...)"
