import pytest
from dappier import Dappier, DappierAsync

def test_dappier_with_api_key():
    api_key = "test_api_key"
    dappier = Dappier(api_key=api_key)
    assert dappier.api_key == api_key

def test_dappier_with_env_variable(monkeypatch):
    api_key = "test_api_key"
    monkeypatch.setenv("DAPPIER_API_KEY", api_key)
    dappier = Dappier()
    assert dappier.api_key == api_key

def test_dappier_without_api_key():
    with pytest.raises(ValueError, match="API key must be provided either as an argument or through the environment variable DAPPIER_API_KEY."):
        Dappier()

def test_dappier_async_with_api_key():
    api_key = "test_api_key"
    dappier = DappierAsync(api_key=api_key)
    assert dappier.api_key == api_key

def test_dappier_async_with_env_variable(monkeypatch):
    api_key = "test_api_key"
    monkeypatch.setenv("DAPPIER_API_KEY", api_key)
    dappier = DappierAsync()
    assert dappier.api_key == api_key

def test_dappier_async_without_api_key():
    with pytest.raises(ValueError, match="API key must be provided either as an argument or through the environment variable DAPPIER_API_KEY."):
        DappierAsync()
