import pytest
from unittest.mock import patch
from dappier import Dappier
from dappier.types import AIModelResponse, REAL_TIME_AI_MODEL, POLYGON_STOCK_MARKET_AI_MODEL

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
    # Mock the response from the API
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "Success"}

    # Instantiate Dappier with the mock API key
    dappier = Dappier(api_key="test_api_key")
    query = "real-time data"
    
    # Perform the search API call
    response = dappier.real_time_search_api(query=query)

    # Construct the expected URL based on REAL_TIME_AI_MODEL
    expected_url = f"https://api.dappier.com/app/aimodel/{REAL_TIME_AI_MODEL}"
    mock_post.assert_called_once_with(
        expected_url,
        headers={"Authorization": "Bearer test_api_key", "Content-Type": "application/json"},
        data='{"query": "real-time data"}'
    )
    
    # Check if the response is an instance of AIModelResponse
    assert isinstance(response, AIModelResponse)
    
    # Validate that the message returned is "Success"
    assert response.message == "Success"


@patch("dappier.api.ai_models.requests.post")
def test_polygon_stock_market_search_api(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "Stock Market Success"}

    dappier = Dappier(api_key="test_api_key")
    query = "stock market data"
    response = dappier.polygon_stock_market_search_api(query=query)

    # Replace BASE_URL with the actual base URL used by the API
    mock_post.assert_called_once_with(
        f"https://api.dappier.com/app/aimodel/{POLYGON_STOCK_MARKET_AI_MODEL}",  # Example URL
        headers={"Authorization": "Bearer test_api_key", "Content-Type": "application/json"},
        data='{"query": "stock market data"}'
    )
    assert isinstance(response, AIModelResponse)
    assert response.message == "Stock Market Success"  # Adjust based on actual response structure

# Test Dappier representation
def test_dappier_repr():
    api_key = "test_api_key"
    dappier = Dappier(api_key=api_key)
    assert repr(dappier) == "Dappier(api_key=test...)"  # The key should be truncated in the representation
