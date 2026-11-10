# Another user must not read the owner's rating.
def test_other_user_cannot_read(api, auth, other_auth, rating):

    path = f"/api/ratings/{rating['id']}"

    denied = api.get(path, headers=other_auth)

    assert 400 <= denied.status_code <= 499

    owner = api.get(path, headers=auth)

    assert owner.status_code == 200
    assert owner.json() == rating


# Another user must not update the owner's rating.
def test_other_user_cannot_update(api, auth, other_auth, rating):

    path = f"/api/ratings/{rating['id']}"

    denied = api.put(
        path,
        json={"stars": 5},
        headers=other_auth
    )

    assert 400 <= denied.status_code <= 499

    owner = api.get(path, headers=auth)

    assert owner.status_code == 200
    assert owner.json()["stars"] == 3


# Another user must not delete the owner's rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):

    path = f"/api/ratings/{rating['id']}"

    denied = api.delete(
        path,
        headers=other_auth
    )

    assert 400 <= denied.status_code <= 499

    owner = api.get(path, headers=auth)

    assert owner.status_code == 200
    assert owner.json() == rating
