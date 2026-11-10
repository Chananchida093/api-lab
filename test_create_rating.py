
import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


def assert_api_error(res, expected_status):
    """Check the status and that a JSON error message is returned."""
    assert res.status_code == expected_status
    body = res.json()
    assert isinstance(body["error"], str)
    assert body["error"].strip() != ""


# C1, C2, C3, C4: Base choice - valid rating.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: Below and above valid stars range.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: Decimal stars.
def test_decimal_stars_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert_api_error(res, 400)


# C2: Stars provided as text.
def test_text_stars_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert_api_error(res, 400)


# C2: Missing stars field.
def test_missing_stars_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert_api_error(res, 400)


# C3: A rating for a nonexistent pizza must be refused.
def test_nonexistent_pizza_refused(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}

    res = api.post("/api/ratings", json=new, headers=auth)

    assert_api_error(res, 400)


# C4: No authentication token.
def test_no_token_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}

    res = api.post("/api/ratings", json=new)

    assert_api_error(res, 401)


# C4: Authentication token with wrong length.
def test_short_token_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    bad_auth = {"Authorization": "token short"}

    res = api.post("/api/ratings", json=new, headers=bad_auth)

    assert_api_error(res, 401)
