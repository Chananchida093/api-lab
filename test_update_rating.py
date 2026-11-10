import pytest


# Boundary values for updating rating stars.
@pytest.mark.parametrize(
    "stars, expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400)
    ]
)
def test_update_rating_boundaries(
    api, auth, rating, stars, expected_status
):

    path = f"/api/ratings/{rating['id']}"

    original_stars = rating["stars"]

    res = api.put(
        path,
        json={"stars": stars},
        headers=auth
    )

    assert res.status_code == expected_status

    # Read the rating again after the update.
    read_res = api.get(path, headers=auth)

    assert read_res.status_code == 200

    if expected_status == 200:
        assert read_res.json()["stars"] == stars
    else:
        assert read_res.json()["stars"] == original_stars