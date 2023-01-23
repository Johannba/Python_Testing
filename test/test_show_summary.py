class TestShowSummary:
    def test_valid_email_should_return_welcome_page(self, client, mock_clubs):
        """
        As we dont have means to assert used templates, we check if our posted email is in response
        """
        valid_email = 'club1@test.com'
        response = client.post('/showSummary', data={'email': valid_email})
        assert response.status_code == 200
        assert valid_email in response.data.decode()

    def test_invalid_email_should_return_index_page_with_error(self, client):
        """
        As we dont have means to assert used templates, we check if the error message is in response
        """
        invalid_email = 'invalid@simplylift.com'
        response = client.post('/showSummary', data={'email': invalid_email})
        assert response.status_code == 200
        assert 'E-mail is unknown, please enter a valid e-mail !' in response.data.decode()
