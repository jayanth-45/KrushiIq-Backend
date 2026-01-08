import json

def test_get_farmer_profile(client):
    """Test retrieving farmer profile."""
    # Add a mock profile to the database
    client.application.db.farmers.insert_one({
        'name': 'John Doe',
        'location': 'Bangalore, Karnataka',
        'land_acres': 2.5,
        'language': 'en'
    })
    
    response = client.get('/api/farmer-profile')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['name'] == 'John Doe'

def test_update_farmer_profile(client):
    """Test updating farmer profile."""
    new_profile = {
        'name': 'Jane Smith',
        'location': 'Mysore, Karnataka',
        'land_acres': 5.0,
        'language': 'kn'
    }
    
    response = client.post(
        '/api/farmer-profile',
        data=json.dumps(new_profile),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['status'] == 'profile updated'
    
    # Verify in DB
    db_profile = client.application.db.farmers.find_one({'name': 'Jane Smith'})
    assert db_profile['location'] == 'Mysore, Karnataka'

def test_update_farmer_profile_missing_fields(client):
    """Test updating farmer profile with missing fields."""
    incomplete_profile = {'name': 'Jane Smith'}
    
    response = client.post(
        '/api/farmer-profile',
        data=json.dumps(incomplete_profile),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'Missing required fields' in data['message']
