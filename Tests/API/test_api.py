from Tests.config.config_log import logger
from Tests.API.users_requests import (
    add_user,
    login_user,
    logout_user,
    get_user_profile,
    update_user_profile,
    delete_user,
)
from Tests.utils.generator import generate_random_email

email = generate_random_email()


def test_add_user():
    r = add_user(email)
    logger.debug("Response ->%s", r)
    logger.info("Email -> %s", email)
    assert r.status_code == 201, f"Expected 201 Created, but got {r.status_code}"


def test_login_user():
    r = login_user(email)
    logger.debug("Response ->%s", r)
    token = r.json()["token"]
    logger.info("Token -> %s\nEmail -> %s", token, email)
    assert r.status_code == 200, f"Expected 200 OK, but got {r.status_code}"


def test_get_user_profile():
    t = login_user(email, True)
    r = get_user_profile(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
    assert r.json()["email"] == email
    assert r.json()["firstName"] == "Test"
    assert r.json()["lastName"] == "User"


def test_update_user_profile():
    t = login_user(email, True)
    r = update_user_profile(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
    assert r.json()["email"] == email
    assert r.json()["firstName"] == "Updated"
    assert r.json()["lastName"] == "Updated"


def test_delete_user():
    r = delete_user(generate_random_email())
    logger.info("Request sent!")
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"


def test_logout_user():
    t = login_user(email, True)
    r = logout_user(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)

    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
