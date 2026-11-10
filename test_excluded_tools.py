import pytest


# The recommended pizza must not use an excluded tool.
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Scissors"]
    ]
)
def test_excluded_tool_is_not_used(api, auth, excluded):

    body = {
        "excludedTools": excluded
    }

    res = api.post(
        "/api/pizza",
        json=body,
        headers=auth
    )

    assert res.status_code == 200

    assert res.json()["pizza"]["tool"] not in excluded

# Excluding all tools should return 400 with a JSON error.
@pytest.mark.xfail(
    reason="Defect 1: all tools excluded returns 500 instead of 400",
    strict=True
)
def test_all_tools_excluded_returns_400(api, auth):

    body = {
        "excludedTools": [
            "Knife",
            "Pizza cutter",
            "Scissors"
        ]
    }

    res = api.post(
        "/api/pizza",
        json=body,
        headers=auth
    )

    assert res.status_code == 400

    assert res.headers["Content-Type"].startswith(
        "application/json"
    )

    assert "error" in res.json()