import os
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from typing import Optional

import asyncio
import logging

from dappier.types import (
    RealTimeDataRequest,
    RealTimeDataResponse,
    AIRecommendationsRequest,
    AIRecommendationsResponse,
    SearchAlgorithm
)
from dappier.api import DappierClient, DappierAsyncClient

class Dappier(AbstractContextManager):
    def __init__(self, api_key: Optional[str] = None) -> None:
        if api_key is None:
            api_key = os.getenv("DAPPIER_API_KEY")

            if api_key is None:
                raise ValueError("API key must be provided either as an argument or through the environment variable DAPPIER_API_KEY.")

        self.api_key = api_key
        self._client = DappierClient(api_key=api_key)
    
    def search_real_time_data(self, query: str, ai_model_id: str) -> Optional[RealTimeDataResponse]:
        try:
            request = RealTimeDataRequest(query=query).model_dump()
            response = self._client.client.post(url=f"app/aimodel/{ai_model_id}", json=request)
            response.raise_for_status()
            return RealTimeDataResponse(**response.json())
        except Exception as e:
            print(f"An error occurred while searching real-time data: {e}")
            return None

    def get_ai_recommendations(self, query: str, data_model_id: str, similarity_top_k: int = 9, ref: Optional[str] = None, num_articles_ref: int = 0, search_algorithm: SearchAlgorithm = "most_recent") -> Optional[AIRecommendationsResponse]:
        try:
            request = AIRecommendationsRequest(
                datamodel_id=data_model_id,
                query=query,
                similarity_top_k=similarity_top_k,
                ref=ref,
                num_articles_ref=num_articles_ref,
                search_algorithm=search_algorithm
            ).model_dump()
            response = self._client.client.post(url=f"app/v2/search?data_model_id={data_model_id}", json=request)
            response.raise_for_status()
            return AIRecommendationsResponse(**response.json())
        except Exception as e:
            print(f"An error occurred while fetching AI recommendations: {e}")
            return None
 
    def __enter__(self):
        """
        Suppport async context management to automatically open the client.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Support async context management to automatically close the client.
        """
        self._client.close()

    def __del__(self):
        if hasattr(self, '_client') and self._client:
            self._client.close()

    def __repr__(self) -> str:
        return f"Dappier(api_key={self.api_key[:4]}...)"  # Mask part of the key for privacy

class DappierAsync(AbstractAsyncContextManager):
    def __init__(self, api_key: Optional[str] = None) -> None:
        if api_key is None:
            api_key = os.getenv("DAPPIER_API_KEY")

            if api_key is None:
                raise ValueError("API key must be provided either as an argument or through the environment variable DAPPIER_API_KEY.")

        self.api_key = api_key
        self._async_client = DappierAsyncClient(api_key=api_key)
    
    async def search_real_time_data_async(self, query: str, ai_model_id: str) -> Optional[RealTimeDataResponse]:
        try:
            request = RealTimeDataRequest(query=query).model_dump()
            response = await self._async_client.client.post(url=f"app/aimodel/{ai_model_id}", json=request)
            response.raise_for_status()
            return RealTimeDataResponse(**response.json())
        except Exception as e:
            print(f"An error occurred while searching real-time data: {e}")

    async def get_ai_recommendations_async(self, query: str, data_model_id: str, similarity_top_k: int = 9, ref: Optional[str] = None, num_articles_ref: int = 0, search_algorithm: SearchAlgorithm = "most_recent") -> Optional[AIRecommendationsResponse]:
        try:
            request = AIRecommendationsRequest(
                datamodel_id=data_model_id,
                query=query,
                similarity_top_k=similarity_top_k,
                ref=ref,
                num_articles_ref=num_articles_ref,
                search_algorithm=search_algorithm
            ).model_dump()
            response = await self._async_client.client.post(url=f"app/v2/search?data_model_id={data_model_id}", json=request)
            response.raise_for_status()
            return AIRecommendationsResponse(**response.json())
    
        except Exception as e:
            print(f"An error occurred while fetching AI recommendations: {e}")
    
    async def __aenter__(self):
        """
        Suppport async context management to automatically open the client.
        """
        return self
  
    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Support async context management to automatically close the client.
        """
        await self._async_client.close()

    def __del__(self):
        """
        Log a warning if the instance is not closed explicitly.
        """
        if hasattr(self, '_async_client') and self._async_client.client and not self._async_client.client.is_closed:
            try:
                asyncio.run(self._async_client.close())
            except Exception as e:
                logging.error("DappierAsync instance was not closed explicitly. Resources may not be cleaned up.")
                logging.error(f"Error while closing DappierAsyncClient: {e}")

    def __repr__(self) -> str:
        return f"DappierAsync(api_key={self.api_key[:4]}...)"  # Mask part of the key for privacy
