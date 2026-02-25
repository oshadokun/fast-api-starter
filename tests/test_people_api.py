def test_create_person(client):
    response = client.post(
        "/people",
        json={"name": "Dayo", "age": 30, "email": "dayo@test.com"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Dayo"
    assert data["age"] == 30
    assert data["email"] == "dayo@test.com"
    assert "id" in data


def test_duplicate_email_returns_400(client):
    r1 = client.post(
        "/people",
        json={"name": "UserOne", "age": 25, "email": "dup@test.com"},
    )
    print("FIRST:", r1.status_code, r1.json())

    r2 = client.post(
        "/people",
        json={"name": "UserTwo", "age": 30, "email": "dup@test.com"},
    )
    print("SECOND:", r2.status_code, r2.json())

    assert r2.status_code == 400


def test_empty_patch_returns_422(client):
    # We don't care if person exists for this specific test.
    # If your route validates "at least one field" at the schema level,
    # it should return 422 before hitting the database.
    response = client.patch("/people/1", json={})
    assert response.status_code == 422