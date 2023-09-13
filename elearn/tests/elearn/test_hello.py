
def test_hello_elearn(client):
    response = client.get("/docs/")
    assert response.status_code == 200
