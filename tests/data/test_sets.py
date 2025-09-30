# tests/data/test_sets.py

import pytest
import pandas as pd
import json
from pathlib import Path
from unittest.mock import patch, Mock

from api_helper.data.sets import fetch_api_v0, fetch_api_v1

@pytest.fixture
def sample_api_response():
    """Simulate a JSON API response with daily and hourly data"""
    return {
        "daily": {
            "time": [1, 2, 3],
            "temperature": [20.5, 21.0, 19.8],
            "rain": [0, 5, 0]
        },
        "hourly": {
            "time": [1, 2, 3],
            "temperature": [20, 21, 19],
            "rain": [0, 1, 0]
        }
    }

def test_fetch_api_v0(sample_api_response):
    """Test fetch_api_v0 returns a DataFrame"""
    with patch("requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = sample_api_response
        mock_get.return_value = mock_resp

        df = fetch_api_v0("http://dummy-url.com", params={})
        assert isinstance(df, pd.DataFrame)
        pd.testing.assert_frame_equal(df, pd.DataFrame(sample_api_response))


def test_fetch_api_v1_with_headers(sample_api_response):
    """Test fetch_api_v1 returns dict of DataFrames with headers"""
    with patch("requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = sample_api_response
        mock_get.return_value = mock_resp

        dfs = fetch_api_v1("http://dummy-url.com", params={}, with_headers=True)
        assert isinstance(dfs, dict)
        for key, df in dfs.items():
            assert isinstance(df, pd.DataFrame)
            if 'time' in df.columns:
                assert pd.api.types.is_datetime64_any_dtype(df['time'])


def test_fetch_api_v1_without_headers(sample_api_response):
    """Test fetch_api_v1 returns dict of DataFrames without headers"""
    with patch("requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = sample_api_response
        mock_get.return_value = mock_resp

        dfs = fetch_api_v1("http://dummy-url.com", params={}, with_headers=False)
        for df in dfs.values():
            # Columns should be integers
            assert all(isinstance(c, int) for c in df.columns)
