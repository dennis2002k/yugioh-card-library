from fastapi.testclient import TestClient

# from app.app import app

# client = TestClient(app)
RANDOM_ID_TO_ADD = 96676583
RANDOM_ID_TO_REMOVE = 32061192
NOT_EXIST_ID = 8402543




def test_get_library(client, auth_headers):

    response = client.get("/me/library", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

def test_add_card_to_library(client, auth_headers):

    response = client.post(
        "/me/library/add",
        headers=auth_headers,
        json={"id": RANDOM_ID_TO_ADD}
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

def test_add_non_existent_card(client, auth_headers):
   
    response = client.post(
        "/me/library/add",
        headers=auth_headers,
        json={"id": 123}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Card does not exist"}

def test_remove_card_from_library(client, auth_headers):

    add_res = client.post(
        "/me/library/add",
        headers=auth_headers,
        json={"id": RANDOM_ID_TO_REMOVE}
    )
    assert add_res.status_code == 200
    response = client.delete(
        f"me/library/delete/{RANDOM_ID_TO_REMOVE}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

def test_remove_card_that_dooesnt_exist(client, auth_headers):

    response = client.delete(
        f"me/library/delete/{NOT_EXIST_ID}",
        headers=auth_headers
    )

    response.status_code == 404
    response.json() == {"detail": "Card not found in user's library"}


def test_card_search_db(client):
    response = client.get("/card/search")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)



