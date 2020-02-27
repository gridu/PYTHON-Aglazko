from urllib.parse import urlencode


def test_login(client, mocker):
    
    get_center_mock = mocker.patch("app.dao.AnimalCentersDAO.get_center_by_login")
    get_center_mock.return_value = {'id': 2}
    mocker.patch("app.dao.AccessRequestDAO.create_access_request")
    check_password_mock = mocker.patch("app.dao.AnimalCentersDAO.check_password")
    check_password_mock.return_value = True
    credentials = {'login': 'anna', 'password': 'abc'}
    response = client.get('/login?{}'.format(urlencode(credentials)))
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_get_animals(client, mocker):
    expected = [
        {
            "age": 5,
            "center_id": 1,
            "description": "ff",
            "id": 4,
            "name": "lokfo",
            "price": 32.0,
            "species_id": 2
        },
        {
            "age": 5,
            "center_id": 1,
            "description": "ff",
            "id": 5,
            "name": "lokf",
            "price": 32.0,
            "species_id": 2
        },
        {
            "age": 5,
            "center_id": 1,
            "description": "ff",
            "id": 6,
            "name": "l",
            "price": 32.0,
            "species_id": 3
        }
    ]

    mock = mocker.patch("app.dao.AnimalsDAO.get_animals")
    mock.return_value = expected
    response = client.get('/animals')
    assert response.status_code == 200
    assert response.json == expected
