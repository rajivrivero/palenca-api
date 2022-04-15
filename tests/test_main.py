from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Palenca"}


def test_success_post_login():
    expected_output = {
        "message": "SUCCESS",
        "access_token": "cTV0aWFuQ2NqaURGRE82UmZXNVBpdTRxakx3V1F5",
    }
    payload = {"email": "pierre@palenca.com", "password": "MyPwdChingon123"}
    response = client.post("/uber/login", json=payload)
    assert response.status_code == 200
    assert response.json() == expected_output


def test_bad_request_post_login():
    expected_output = {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "value is not a valid email address",
                "type": "value_error.email",
            },
            {
                "loc": ["body", "password"],
                "msg": "ensure this value has at least 5 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 5},
            },
        ]
    }
    payload = {"email": "", "password": ""}
    response = client.post("/uber/login", json=payload)
    assert response.status_code == 422
    assert response.json() == expected_output


def test_unauthorized_post_login():
    expected_output = {"detail": "Unauthorized"}
    payload = {"email": "unauthorized@user.com", "password": "password"}
    response = client.post("/uber/login", json=payload)
    assert response.status_code == 401
    assert response.json() == expected_output


def test_get_profile():
    expected_output = {
        "message": "SUCCESS",
        "platform": "uber",
        "profile": {
            "country": "mx",
            "city_name": "Ciudad de México",
            "worker_id": "34dc0c89b16fd170eba320ab186d08ed",
            "first_name": "Pierre",
            "last_name": "Delarroqua",
            "email": "pierre@palenca.com",
            "phone_prefix": "+52",
            "phone_number": "5576955981",
            "rating": "4.8",
            "lifetime_trips": 1254,
        },
    }
    respose = client.get("/uber/profile/cTV0aWFuQ2NqaURGRE82UmZXNVBpdTRxakx3V1F5")
    assert respose.status_code == 200
    assert respose.json() == expected_output


def test_get_invalid_access_token():
    expected_output = {
        "detail": {"message": "CREDENTIALS_INVALID", "details": "Incorrect token"}
    }
    respose = client.get("/uber/profile/invalidtoken")
    assert respose.status_code == 401
    assert respose.json() == expected_output
