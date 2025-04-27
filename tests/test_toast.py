from flask import Flask
from flask.testing import FlaskClient

from tests import app
from tests import client
from tests import logger

def test_toast_new(app: Flask, client: FlaskClient):
    body = {
        "body": "toast for Johnny"
        , "user_id": 1
    }
    response = client.post("/toast/new", json=body)

    assert response.json["body"] == body["body"]
    assert response.json["user_id"] == body["user_id"]
    assert response.json["status"] == "UNREAD"


def test_toast_new_system(app: Flask, client: FlaskClient):
    body = {
        "body": "system toast"
        , "user_id": -1
    }
    response = client.post("/toast/new", json=body)

    assert response.json["body"] == body["body"]
    assert response.json["user_id"] == body["user_id"]
    assert response.json["status"] == "UNREAD"


def test_toast_mark_read_for_user(app: Flask, client: FlaskClient):
    toast_system_id = client.post("/toast/new", json={"body": "toast system", "user_id": -1}).json["id"]
    toast_johnny_id = client.post("/toast/new", json={"body": "toast for Johnny", "user_id": 1}).json["id"]
    toast_kate_id = client.post("/toast/new", json={"body": "toast for Kate", "user_id": 2}).json["id"]

    response = client.put("/toast/mark_read_all", json={"user_id": 1})
    assert response.json["marked_read"] == 1

    toast_system = client.get(f"/toast/{toast_system_id}", content_type="application/json").json
    assert toast_system["status"] == "UNREAD"

    toast_johnny = client.get(f"/toast/{toast_johnny_id}", content_type="application/json").json
    assert toast_johnny["status"] == "READ"

    toast_kate = client.get(f"/toast/{toast_kate_id}", content_type="application/json").json
    assert toast_kate["status"] == "UNREAD"


def test_toast_mark_read_system(app: Flask, client: FlaskClient):
    toast_system_id = client.post("/toast/new", json={"body": "toast system", "user_id": -1}).json["id"]
    toast_johnny_id = client.post("/toast/new", json={"body": "toast for Johnny", "user_id": 1}).json["id"]
    toast_kate_id = client.post("/toast/new", json={"body": "toast for Kate", "user_id": 2}).json["id"]

    response = client.put("/toast/mark_read_all", json={"user_id": -1})
    assert response.json["marked_read"] == 1

    toast_system = client.get(f"/toast/{toast_system_id}", content_type="application/json").json
    assert toast_system["status"] == "READ"

    toast_johnny = client.get(f"/toast/{toast_johnny_id}", content_type="application/json").json
    assert toast_johnny["status"] == "UNREAD"

    toast_kate = client.get(f"/toast/{toast_kate_id}", content_type="application/json").json
    assert toast_kate["status"] == "UNREAD"


def test_toast_get_all(app: Flask, client: FlaskClient):
    toast_system_id_1 = client.post("/toast/new", json={"body": "toast system 1", "user_id": -1}).json["id"]
    toast_system_id_2 = client.post("/toast/new", json={"body": "toast system 2", "user_id": -1}).json["id"]
    toast_kate_id_1 = client.post("/toast/new", json={"body": "toast for Kate 1", "user_id": 2}).json["id"]
    toast_kate_id_2 = client.post("/toast/new", json={"body": "toast for Kate 2", "user_id": 2}).json["id"]
    client.post("/toast/new", json={"body": "toast for Johnny", "user_id": 1})

    system_ids = [toast_system_id_1, toast_system_id_2]

    toasts_system = client.get(f"/toast/all?user_id={-1}", content_type="application/json").json
    assert len(toasts_system) == len(system_ids)

    for toast in toasts_system:
        assert toast["id"] in system_ids
        system_ids.remove(toast["id"])

    kate_ids = [toast_kate_id_1, toast_kate_id_2]

    toasts_kate = client.get(f"/toast/all?user_id={2}", content_type="application/json").json
    assert len(toasts_kate) == len(kate_ids)

    for toast in toasts_kate:
        assert toast["id"] in kate_ids
        kate_ids.remove(toast["id"])
