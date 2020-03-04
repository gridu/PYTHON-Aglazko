"""API tests"""

from urllib.parse import urlencode


def test_login(client, mocker):
    """This test checks that login is working, and returns correct status code
    and access_token in response json"""
    get_center_mock = mocker.patch("app.dao_models.AnimalCenterORM.get_center_by_login")
    get_center_mock.return_value = {'id': 2}
    check_password = mocker.patch("app.dao_models.AnimalCenterORM.check_password")
    check_password.return_value = True
    mocker.patch("app.dao.AccessRequestDAO.create_access_request")
    check_password_mock = mocker.patch("app.dao.AnimalCentersDAO.check_password")
    check_password_mock.return_value = True
    credentials = {'login': 'anna', 'password': 'abc'}
    response = client.get('/login?{}'.format(urlencode(credentials)))
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_get_animals(client, mocker):
    """This test checks that animals are returned as expected"""
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

    mock = mocker.patch("app.dao_models.AnimalORM.get_animals")
    mock.return_value = expected
    response = client.get('/animals')
    assert response.status_code == 200
    assert response.json == expected


def test_get_species_info(client, mocker):
    """This test check that species info returns as it should be"""
    expected = [
    {
        "description": "good cat",
        "id": 1,
        "name": "cat",
        "price": 160.0
    },
    [
        {
            "id": 1,
            "name": "toto"
        },
        {
            "id": 2,
            "name": "momo"
        },
        {
            "id": 4,
            "name": "jojo"
        },
        {
            "id": 5,
            "name": "1"
        }
    ]
    ]
    mock = mocker.patch("app.dao_models.SpeciesORM.get_species_inform")
    mock.return_value = expected
    response = client.get('/species/1')
    assert response.status_code == 200
    assert response.json == expected