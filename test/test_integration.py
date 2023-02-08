def test_login_logout(client, mock_clubs, captured_templates):
    response = client.post("/showSummary", data={"email": mock_clubs[0]["email"]})
    template, context = captured_templates[0]
    assert response.status_code == 200
    assert template.name == "welcome.html"

    response = client.get("logout")
    template, context = captured_templates[0]
    assert response.status_code == 302


def test_purchase_two_time_same_competitions(
    client, mock_clubs, mock_competitions, captured_templates
):
    places_required = 2
    initial_points = int(mock_clubs[0]["points"])
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": mock_competitions[0]["name"],
            "club": mock_clubs[0]["name"],
            "places": places_required,
        },
    )
    template, context = captured_templates[0]
    assert response.status_code == 200
    assert template.name == "welcome.html"
    assert context["club"]["points"] == str(initial_points - places_required)

    places_required = 3
    initial_points = int(mock_clubs[0]["points"])
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": mock_competitions[0]["name"],
            "club": mock_clubs[0]["name"],
            "places": places_required,
        },
    )
    template, context = captured_templates[0]
    assert response.status_code == 200
    assert template.name == "welcome.html"
    assert context["club"]["points"] == str(initial_points - places_required)


def test_purchase_two_time_two_competitions(
    client, mock_clubs, mock_competitions, captured_templates
):
    places_required = 2
    initial_points = int(mock_clubs[0]["points"])
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": mock_competitions[1]["name"],
            "club": mock_clubs[0]["name"],
            "places": places_required,
        },
    )
    template, context = captured_templates[0]
    assert response.status_code == 200
    assert template.name == "welcome.html"
    assert context["club"]["points"] == str(initial_points - places_required)

    places_required = 3
    initial_points = int(mock_clubs[0]["points"])
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": mock_competitions[0]["name"],
            "club": mock_clubs[0]["name"],
            "places": places_required,
        },
    )
    template, context = captured_templates[0]
    assert response.status_code == 200
    assert template.name == "welcome.html"
    assert context["club"]["points"] == str(initial_points - places_required)


def test_updating_of_board_after_purchase(
    client, mock_clubs, mock_competitions, captured_templates
):
    places_required = 2
    initial_club_points = int(mock_clubs[0]["points"])
    initial_competition_place = int(mock_competitions[0]["numberOfPlaces"])
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": mock_competitions[0]["name"],
            "club": mock_clubs[0]["name"],
            "places": places_required,
        },
    )
    template, context = captured_templates[0]
    assert response.status_code == 200
    assert template.name == "welcome.html"
    assert context["club"]["points"] == str(initial_club_points - places_required)

    response = client.get("/board")
    template, context = captured_templates[1]
    assert response.status_code == 200
    assert template.name == "board.html"
    assert context["clubs"][0]["points"] == str(initial_club_points - places_required)
    assert context["competitions"][0]["numberOfPlaces"] == str(
        initial_competition_place - places_required
    )
