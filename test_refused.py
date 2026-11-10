import uuid


# A duplicate username must be refused.
def test_duplicate_username(api):

    name = "lab-" + uuid.uuid4().hex[:12]

    user = {
        "username": name,
        "password": "Pizza-2026"
    }

    first = api.post("/api/users", json=user)
    assert first.status_code == 201

    second = api.post("/api/users", json=user)

    assert second.status_code == 400
    assert second.json() == {
        "error": "username already taken"
    }


# Logging in with a wrong password must be refused.
def test_wrong_password(api):

    name = "lab-" + uuid.uuid4().hex[:12]

    user = {
        "username": name,
        "password": "Pizza-2026"
    }

    created = api.post("/api/users", json=user)
    assert created.status_code == 201

    wrong = {
        "username": name,
        "password": "WrongPassword"
    }

    res = api.post(
        "/api/users/token/login",
        json=wrong
    )

    assert res.status_code == 401
    assert res.json() == {
        "error": "authentication failed"
    }


# An empty username must be refused.
def test_empty_username(api):

    user = {
        "username": "",
        "password": "Pizza-2026"
    }

    res = api.post("/api/users", json=user)

    assert res.status_code == 400
    assert res.json() == {
        "error": "username field is empty"
    }