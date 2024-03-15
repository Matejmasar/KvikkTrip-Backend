import pytest
from database import db
from flask import Flask
from app import app


@pytest.fixture()
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()

    with app.app_context():
        db.create_all()

def test_deploying(client):
    with app.app_context():
        response = client.get("/")
        print(response.data)
        assert b"Kvikk Trip Backend" in response.data

def test_getting_locations(client):
    with app.app_context():
        response = client.get("/location")
        print(response.data)
        assert b"Voss" in response.data

def test_posting_location(client):
    with app.app_context():
        response = client.post("/location", json={
            "name": "ABCD",
            "latitude": "1234",
            "longitude": "12345"
        })
        assert response.json["name"] == "ABCD"
        assert response.json["latitude"] == "1234"
        assert response.json["longitude"] == "1235"


def test_putting_location(client):
    with app.app_context():
        response = client.put("/location/1", json={
            "name": "Boom2",
            "latitude": "1",
            "longitude": "1.5"
        })
        assert response.json["name"] == "Boom2"
        assert response.json["latitude"] == "1"
        assert response.json["longitude"] == "1.5"


def test_deleting_location(client):
    with app.app_context():
        response = client.delete("/location/4")
        assert response.json["name"] == "ABCD"
        response = client.get("/location/4")
        "assert not found"
