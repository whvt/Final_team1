"""Tests API"""

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
    """
    test add user
    """
    r_email = add_user(email)
    logger.debug("Response ->%s", r_email)
    logger.info("Email -> %s", email)
    assert r_email.status_code == 201, f"Expected 201 Created, but got {r_email.status_code}"


def test_add_user_empty_firstname():
    """
    test add user with empty firstname
    """
    empty_firstname = ''
    r_firstname = add_user(email, firstname=empty_firstname)
    logger.info("Firstname field is empty -> %s", empty_firstname)
    logger.debug("Response ->%s", r_firstname)
    assert (
        r_firstname.status_code == 400
    ), f"Expected 400 Created, but got {r_firstname.status_code}"


def test_add_user_empty_lastname():
    """
    test add user with empty lastname
    """
    empty_lastname = ''
    r_lastname = add_user(email, lastname=empty_lastname)
    logger.info("Firstname field is empty -> %s", empty_lastname)
    logger.debug("Response ->%s", r_lastname)
    assert r_lastname.status_code == 400, f"Expected 400 Created, but got {r_lastname.status_code}"


def test_add_user_empty_password():
    """
    test add user with empty password
    """
    empty_password = ''
    r_password = add_user(email, password=empty_password)
    logger.info("Password field is empty -> %s", empty_password)
    logger.debug("Response ->%s", r_password)
    assert r_password.status_code == 400, f"Expected 400 Created, but got {r_password.status_code}"


def test_add_user_short_password():
    """
    test add user with short password
    """
    short_password = '22'
    r_password = add_user(email, password=short_password)
    logger.info("Password is too short -> %s", short_password)
    logger.debug("Response ->%s", r_password )
    value = int(len(r_password.json()["errors"]['password']['value']))
    message = r_password .json()["errors"]['password']['message']
    assert value < 8 , f"Password length must be lesser than 5, but got {message}"


def test_add_user_empty_email():
    """
    test add user with empty email
    """
    empty_email = ''
    r_email = add_user(empty_email)
    logger.info("Email field is empty -> %s", empty_email)
    logger.debug("Response ->%s", r_email)
    assert r_email.status_code == 400, f"Expected 400 Created, but got {r_email.status_code}"


def test_add_user_invalid_email():
    """
    test add user with invalid email
    """
    invalid_email = 'test@'
    r_invalid_email = add_user(invalid_email)
    logger.info("Invalid Email  -> %s", invalid_email)
    logger.debug("Response ->%s", r_invalid_email)
    assert (
        r_invalid_email.status_code == 400
    ), f"Expected 400 Created, but got {r_invalid_email.status_code}"


def test_login_user():
    """
    test login user
    """
    r_login_user = login_user(email)
    logger.debug("Response ->%s", r_login_user)
    token = r_login_user.json()["token"]
    logger.info("Token -> %s\nEmail -> %s", token, email)
    assert r_login_user.status_code == 200, f"Expected 200 OK, but got {r_login_user.status_code}"
    assert token


def test_login_user_email_invalid():
    """
    test login user with invalid email
    """
    email_invalid = 'email'
    r_email_invalid = login_user(email_invalid)
    logger.info("Invalid Email  -> %s", email_invalid)
    logger.debug("Response ->%s", email_invalid)
    assert r_email_invalid is None, f"Expected None object, but got {r_email_invalid}"


def test_login_user_email_not_exist():
    """
    test login user with not existing email
    """
    email_not_exist = 'not_exist_email@bk.ru'
    r_not_exist = login_user(email_not_exist)
    logger.info("Email not exist  -> %s", email_not_exist)
    logger.debug("Response ->%s", email_not_exist)
    assert r_not_exist is None, f"Expected None object, but got {r_not_exist}"


def test_login_user_email_field_empty():
    """
    test login user with empty email field
    """
    email_field_empty = ''
    r_email_field_empty = login_user(email_field_empty)
    logger.info("Email field is empty -> %s", email_field_empty)
    logger.debug("Response ->%s", email_field_empty)
    assert r_email_field_empty is None, f"Expected None object, but got {r_email_field_empty}"


def test_login_user_invalid_password():
    """
    test login user with invalid password
    """
    invalid_password = 'not_exist_email@bk.ru'
    r_invalid_password = login_user(email, password=invalid_password)
    logger.info("Invalid password  -> %s", invalid_password)
    logger.debug("Response ->%s", invalid_password)
    assert r_invalid_password is None, f"Expected None object, but got {r_invalid_password}"


def test_login_user_invalid_token():
    """
    test login user with invalid token
    """
    t = login_user(email, True)
    invalid_token = 'invalid_token'
    r = logout_user(invalid_token )
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)
    assert r.status_code == 401, f"Expected 401 OK {r.status_code}"


def test_get_user_profile():
    """
    test get user profile
    """
    t = login_user(email, True)
    r = get_user_profile(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
    assert r.json()["email"] == email
    assert r.json()["firstName"] == "Test"
    assert r.json()["lastName"] == "User"


def test_get_user_profile_after_logout():
    """
    test get user profile after logout
    """
    t = login_user(email, True)
    logout_user(t)
    logger.info("Logged out!")
    log_out = get_user_profile(t)
    logger.info("Logged out status! Request sent!")
    logger.debug("Token used ->%s", t)
    assert log_out.status_code == 401, f"Expected 401 -Logout OK {log_out.status_code}"


def test_get_user_profile_unauthorized():
    """
    test get user profile being unauthorized
    """
    unauthorized = get_user_profile('invalid_token')
    logger.info("Logged out status, invalid_token! Request sent!")
    logger.debug("Response ->%s", unauthorized)
    assert unauthorized.status_code == 401, f"Expected 401 Unauthorized {unauthorized.status_code}"


def test_update_user_profile():
    """
    test update user profile
    """
    t = login_user(email, True)
    r = update_user_profile(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
    assert r.json()["email"] == email
    assert r.json()["firstName"] == "Updated"
    assert r.json()["lastName"] == "Updated"


def test_update_user_profile_firstname_new():
    """
    test update user profile with new firstname data
    """
    t = login_user(email, True)
    update_user_profile(t)
    firstname_new = "TestUpdated"
    r = update_user_profile(t, firstname=firstname_new)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Firstname field updated ->%s", firstname_new)
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
    assert r.json()["email"] == email
    assert r.json()["firstName"] == firstname_new
    assert r.json()["lastName"] == "Updated"


def test_update_user_profile_empty_req_body():
    """
    test update user profile with empty request body
    """
    t = login_user(email, True)
    firstname_empty = ''
    lastname_empty = ''
    r = update_user_profile(t, firstname=firstname_empty, lastname=lastname_empty)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Firstname empty field updated ->%s", firstname_empty)
    logger.debug("Lastname empty fields updated ->%s", lastname_empty)
    logger.debug("Response ->%s", r)
    assert r.status_code == 400, f"Expected 400 OK {r.status_code}"


def test_update_user_profile_empty_request_body():
    """
    test update user profile with empty request body
    """
    t = login_user(email, True)
    invalid_token = 'invalid_token'
    invalid_token_request = update_user_profile(invalid_token)
    logger.info("Logged out status! Request sent!")
    logger.debug("Token used ->%s", t)
    assert (
        invalid_token_request.status_code == 401
    ), f"Expected 401 -Logout OK {invalid_token_request.status_code}"


def test_update_user_profile_unauthorized():
    """
    test update user profile being unauthorized
    """
    unauthorized = update_user_profile('invalid_token')
    logger.info("Logged out status, invalid_token! Request sent!")
    logger.debug("Response ->%s", unauthorized)
    assert unauthorized.status_code == 401, f"Expected 401 Unauthorized {unauthorized.status_code}"


def test_logout_user():
    """
    test logout user
    """
    t = login_user(email, True)
    r = logout_user(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"


def test_logout_user_repeated():
    """
    test logout user repeated request
    """
    t = login_user(email, True)
    r = logout_user(t)
    repeat_log_out = logout_user(t)
    logger.info("Request sent!")
    logger.debug("Token used ->%s", t)
    logger.debug("Response ->%s", repeat_log_out)
    assert repeat_log_out.status_code == 401, f"Expected 401 OK {r.status_code}"


def test_delete_user():
    """
    test delete user
    """
    r = delete_user(generate_random_email())
    logger.info("Request sent!")
    logger.debug("Response ->%s", r)
    assert r.status_code == 200, f"Expected 200 OK {r.status_code}"
