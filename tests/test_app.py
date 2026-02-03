from fastapi.testclient import TestClient

# from app.app import app

# client = TestClient(app)
RANDOM_ID_TO_ADD = 96676583
RANDOM_ID_TO_REMOVE = 32061192
NOT_EXIST_ID = 8402543


def test_user_full_journey(client, test_cards):
    # 1. REGISTER a new user
    user_data = {"username": "bridge_boy", "password": "supersecretpassword", "email": "supersecretemail@gmail.com"}
    reg_response = client.post("/register", data=user_data)
    assert reg_response.status_code == 200, f"Registration failed: {reg_response.text}"

    # 2. LOGIN to get the Access Token
    login_response = client.post(
        "/token", 
        data={"username": "bridge_boy", "password": "supersecretpassword"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. ADD A CARD to the library
    # (Ensure this ID exists in your seeded/test DB)
    card_id = RANDOM_ID_TO_ADD 
    add_response = client.post(
        "/me/library/add", 
        headers=headers, 
        json={"id": card_id}
    )
    assert add_response.status_code == 200
    assert add_response.json()["success"] is True

    # 4. VERIFY the card is actually in the library
    lib_response = client.get("/me/library", headers=headers)
    assert lib_response.status_code == 200
    
    # Check if the card ID is in the list of card objects returned
    library_ids = [card["id"] for card in lib_response.json()]
    assert card_id in library_ids
    print("\n✅ Golden Path Verified: User can register, login, and manage cards!")


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



