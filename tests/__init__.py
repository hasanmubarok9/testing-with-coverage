import pytest

from flask import Flask, request, json
from app import app, db

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def reset_database():

    db.drop_all()

    db.create_all()


