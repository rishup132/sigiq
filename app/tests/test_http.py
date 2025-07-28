import os
import pytest
from django.test import Client

@pytest.fixture
def client():
    return Client()

def test_healthz(client):
    res = client.get("/healthz/")
    assert res.status_code == 200
    assert res.content == b'{"status": "ok"}'

def test_version(client):
    res = client.get("/version/")
    assert res.status_code == 200
    assert res.content.decode() == '{"version": "unknown"}'

def test_metrics_raw(client):
    res = client.get("/metrics/")
    assert res.status_code == 200