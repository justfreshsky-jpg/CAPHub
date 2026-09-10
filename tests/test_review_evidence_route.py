from app import app


def test_review_evidence_route_is_public_json_without_user_content():
    client = app.test_client()

    response = client.get('/review-evidence')

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['product_id'] == 'civicops'
    assert payload['tool_count'] == 3
    assert payload['tools'][0]['release_state'] == 'reviewed_source_leads'
    assert 'not an operational authorization' in payload['notice']
    assert 'meeting context' not in response.get_data(as_text=True).lower()
