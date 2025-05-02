import os
import json
from assignment_code.extract import fetch_disease_data, CACHE_FILE

def test_fetch_disease_data_one_page(monkeypatch):
    import requests

    # Create a generator that returns 1 page of data, then an empty list
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, data):
                self.status_code = 200
                self._data = data
            def json(self):
                return self._data
        # simulate one valid page, then an empty one
        if not hasattr(mock_get, "called"):
            mock_get.called = True
            return MockResponse([{"topic": "Diabetes", "locationabbr": "NY"}])
        else:
            return MockResponse([])

    monkeypatch.setattr(requests, "get", mock_get)

    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

    fetch_disease_data(topics=["Diabetes"], limit=10)

    assert os.path.exists(CACHE_FILE)
    with open(CACHE_FILE) as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 1
