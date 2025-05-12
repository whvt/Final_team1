import pytest
from Tests.config.config_log import logger
from Tests.API.users_requests import add_user, login_user
from Tests.API.contacts_requests import (
    add_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact,
    add_contact_with_payload
)
from Tests.utils.generator import generate_random_email

user_email = generate_random_email()


def setup_module():
    add_user(user_email)
    logger.info("Test user created with email: %s", user_email)


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact():
    token = login_user(user_email, True)
    r = add_contact(token)
    logger.info("Contact creation request sent!")
    logger.debug("Response -> %s", r.text)

    assert r.status_code == 201, f"Expected 201 Created, but got {r.status_code}"
    assert "firstName" in r.json(), "firstName field is missing in response"
    assert "lastName" in r.json(), "lastName field is missing in response"
    assert r.json()["firstName"] == "Test"
    assert r.json()["lastName"] == "Contact"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_without_street2():
    token = login_user(user_email, True)
    payload = {
        "firstName": "Test",
        "lastName": "Contact",
        "email": "test.contact@example.com",
        "phone": "1234567890",
        "street1": "Main Street"
    }
    r = add_contact_with_payload(token, payload)

    assert r.status_code == 201, f"Expected 201 Created, but got {r.status_code}"
    assert "street1" in r.json(), "street1 field is missing in response"
    assert ("street2" not in r.json() or r.json()["street2"]
            is None), "street2 should be absent or null"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_without_required_field():
    token = login_user(user_email, True)
    payload = {
        "lastName": "Contact",
        "email": generate_random_email(),
        "phone": "1234567890"
    }
    r = add_contact_with_payload(token, payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_invalid_email():
    token = login_user(user_email, True)
    payload = {
        "firstName": "Test",
        "lastName": "Contact",
        "email": "invalid.email@",
        "phone": "1234567890"
    }
    r = add_contact_with_payload(token, payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_invalid_birthdate():
    token = login_user(user_email, True)
    payload = {
        "firstName": "Test",
        "lastName": "Contact",
        "email": generate_random_email(),
        "phone": "1234567890",
        "birthdate": "01-01-1970"
    }
    r = add_contact_with_payload(token, payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_invalid_phone():
    token = login_user(user_email, True)
    payload = {
        "firstName": "Test",
        "lastName": "Contact",
        "email": generate_random_email(),
        "phone": "123abc4567"
    }
    r = add_contact_with_payload(token, payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_empty_body():
    token = login_user(user_email, True)
    payload = {}
    r = add_contact_with_payload(token, payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_add_contact_without_lastname():
    token = login_user(user_email, True)
    payload = {
        "firstName": "Test",
        "email": generate_random_email(),
        "phone": "1234567890"
    }

    r = add_contact_with_payload(token, payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_get_contacts_no_auth():
    r = get_contacts(None)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_get_contacts_invalid_token():
    r = get_contacts("invalid_token")

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_get_contacts_response_structure():
    token = login_user(user_email, True)
    add_contact(token)

    r = get_contacts(token)

    assert r.status_code == 200, f"Expected 200 OK, but got {r.status_code}"
    assert isinstance(r.json(), list), "Expected a list of contacts"

    if len(r.json()) > 0:
        contact = r.json()[0]
        assert "firstName" in contact, "firstName field is missing"
        assert "lastName" in contact, "lastName field is missing"
        assert "email" in contact, "email field is missing"
        assert "_id" in contact, "_id field is missing"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_get_contact_by_id_no_auth():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    r = get_contact_by_id(None, contact_id)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_get_contact_by_id_invalid_token():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    r = get_contact_by_id("invalid_token", contact_id)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_get_contact_by_nonexistent_id():
    token = login_user(user_email, True)
    nonexistent_id = "60d21b4667d0d8992e610c85"

    r = get_contact_by_id(token, nonexistent_id)

    assert r.status_code == 404, f"Expected 404 Not Found, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_update_contact_put():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]
    new_email = generate_random_email()

    payload = {
        "firstName": "PutUpdated",
        "lastName": "PutContact",
        "email": new_email,
        "phone": "9876543210"
    }
    r = update_contact(token, contact_id, method="put", payload=payload)

    assert r.status_code == 200, f"Expected 200 OK, but got {r.status_code}"
    assert r.json()["firstName"] == "PutUpdated"
    assert r.json()["lastName"] == "PutContact"
    assert r.json()["email"] == new_email

    get_response = get_contact_by_id(token, contact_id)
    assert get_response.json()["firstName"] == "PutUpdated"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_update_contact_no_auth():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    payload = {
        "firstName": "Updated",
        "lastName": "Contact"
    }
    r = update_contact(None, contact_id, payload=payload)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_update_contact_invalid_token():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    payload = {
        "firstName": "Updated",
        "lastName": "Contact"
    }
    r = update_contact("invalid_token", contact_id, payload=payload)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_update_nonexistent_contact():
    token = login_user(user_email, True)
    nonexistent_id = "60d21b4667d0d8992e610c85"

    payload = {
        "firstName": "Updated",
        "lastName": "Contact"
    }
    r = update_contact(token, nonexistent_id, payload=payload)

    assert r.status_code == 404, f"Expected 404 Not Found, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_update_contact_invalid_email():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    payload = {
        "firstName": "Updated",
        "lastName": "Contact",
        "email": "invalid.email@"
    }
    r = update_contact(token, contact_id, payload=payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_update_contact_empty_body():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    payload = {}
    r = update_contact(token, contact_id, payload=payload)

    assert r.status_code == 400, f"Expected 400 Bad Request, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_patch_contact_partial_update():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]
    original_email = contact_response.json()["email"]

    payload = {
        "firstName": "PatchUpdated"
    }
    r = update_contact(token, contact_id, method="patch", payload=payload)

    assert r.status_code == 200, f"Expected 200 OK, but got {r.status_code}"
    assert r.json()["firstName"] == "PatchUpdated"
    assert r.json()["email"] == original_email


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_patch_contact_multiple_fields():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]
    new_emeil = generate_random_email()
    new_phone = "5555555555"
    payload = {
        "email": new_emeil,
        "phone": new_phone
    }
    r = update_contact(token, contact_id, method="patch", payload=payload)

    assert r.status_code == 200, f"Expected 200 OK, but got {r.status_code}"
    assert r.json()["email"] == new_emeil
    assert r.json()["phone"] == new_phone
    assert r.json()["firstName"] == "Test"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_delete_contact_no_auth():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    r = delete_contact(None, contact_id)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.auth
@pytest.mark.regression
def test_delete_contact_invalid_token():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    r = delete_contact("invalid_token", contact_id)

    assert r.status_code == 401, f"Expected 401 Unauthorized, but got {r.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_delete_contact_twice():
    token = login_user(user_email, True)
    contact_response = add_contact(token)
    contact_id = contact_response.json()["_id"]

    r1 = delete_contact(token, contact_id)
    assert r1.status_code == 200, f"Expected 200 OK, but got {r1.status_code}"

    r2 = delete_contact(token, contact_id)
    assert r2.status_code == 404, f"Expected 404 Not Found, but got {r2.status_code}"


@pytest.mark.apitests
@pytest.mark.contact_management
@pytest.mark.regression
def test_delete_nonexistent_contact():
    token = login_user(user_email, True)
    nonexistent_id = "60d21b4667d0d8992e610c85"

    r = delete_contact(token, nonexistent_id)

    assert r.status_code == 404, f"Expected 404 Not Found, but got {r.status_code}"
