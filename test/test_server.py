class TestShowSummary:
    def test_valid_email_should_return_welcome_page(self, client, mock_clubs, captured_templates):
        """
        As we dont have means to assert used templates, we check if our posted email is in response
        """
        response = client.post('/showSummary', data={'email': mock_clubs[0]['email']})
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club'] == mock_clubs[0]
        assert mock_clubs[0]['email'] in response.data.decode()

    def test_invalid_email_should_return_index_page_with_error(self, client, captured_templates):
        """
        As we dont have means to assert used templates, we check if the error message is in response
        """
        invalid_email = 'invalid@simplylift.com'
        response = client.post('/showSummary', data={'email': invalid_email})
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'index.html'
        assert 'E-mail is unknown, please enter a valid e-mail !' in response.data.decode()
        
class TestPurchasePlaces:
    def test_purchase_less_than_12_places(self, client, mock_clubs, mock_competitions, captured_templates):
        places_required= 2
        initial_points = int(mock_clubs[0]['points'])
        response = client.post('/purchasePlaces', data={
          "competition": mock_competitions[0]['name'],
          "club": mock_clubs[0]['name'],
          "places": places_required})
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club']['points'] == str(initial_points - places_required)
        
    def test_purchase_more_than_12_places(self, client, mock_clubs, mock_competitions, captured_templates):
        places_required= 13
        initial_points = int(mock_clubs[1]['points'])
        response = client.post('/purchasePlaces', data={
          "competition": mock_competitions[0]['name'],
          "club": mock_clubs[1]['name'],
          "places": places_required})
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club']['points'] == str(initial_points)
        
    def test_purchase_more_than_points_places(self, client, mock_clubs, mock_competitions, captured_templates):
        places_required= 13
        initial_points = int(mock_clubs[0]['points'])
        response = client.post('/purchasePlaces', data={
          "competition": mock_competitions[0]['name'],
          "club": mock_clubs[0]['name'],
          "places": places_required})
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club']['points'] == str(initial_points)
        
        
class TestBookCompetition:
    def test_not_book_a_old_competition(self, client, mock_clubs, mock_competitions, captured_templates):
        response = client.get(f"/book/{mock_competitions[1]['name']}/{mock_clubs[0]['name']}")
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert 'You cannot book places in a past competition' in response.data.decode()
        
    def test_book_a_futur_competition(self, client, mock_clubs, mock_competitions, captured_templates):
        response = client.get(f"/book/{mock_competitions[2]['name']}/{mock_clubs[0]['name']}")
        template, context = captured_templates[0]
        assert response.status_code == 200
        assert template.name == 'booking.html'
        assert context['club'] == mock_clubs[0]
        assert context['competition'] == mock_competitions[2]
        