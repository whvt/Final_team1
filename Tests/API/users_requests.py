import json
import requests
from Tests.config.config_log import logger
from Tests.config.env import Env


def add_user(em):
    """Creates a new user."""
    endpoint = "/users"
    payload = json.dumps(
        {
            "firstName": "Test",
            "lastName": "User",
            "email": em,
            "password": "myPassword",
        }
    )
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            f"{Env.URL}{endpoint}", headers=headers, data=payload, timeout=5
        )
        logger.debug("User Created -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def login_user(email, parse_flag=False):
    endpoint = "/users/login"
    payload = json.dumps({"email": email, "password": "myPassword"})
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            f"{Env.URL}{endpoint}", headers=headers, data=payload, timeout=5
        )

        logger.debug("Status Code -> %s", response.status_code)
        logger.debug("Headers -> %s", response.headers)
        logger.debug("Raw Response -> %s", response.text)

        if response.status_code != 200:
            logger.error("Request failed! Status Code: %s", response.status_code)
            return None

        if not response.text.strip():
            logger.error("Empty response received, cannot parse JSON.")
            return None

        return response.json().get("token") if parse_flag else response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def get_user_profile(token):
    """Retrieves user profile details."""
    endpoint = "/users/me"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{Env.URL}{endpoint}", headers=headers, timeout=10)
        logger.debug("User Profile Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def update_user_profile(token):
    """Updates user profile details."""
    endpoint = "/users/me"
    payload = json.dumps({"firstName": "Updated", "lastName": "Updated"})
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.patch(
            f"{Env.URL}{endpoint}", headers=headers, data=payload, timeout=10
        )
        logger.debug("Update Profile Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def delete_user(email):
    add_user(email)
    t = login_user(email).json()["token"]
    endpoint = "/users/me"
    payload = {}
    headers = {"Authorization": f"Bearer {t}"}
    try:
        response = requests.delete(
            f"{Env.URL}{endpoint}", headers=headers, data=payload, timeout=5
        )
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def logout_user(token):
    """Logs out the user."""
    endpoint = "/users/logout"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(f"{Env.URL}{endpoint}", headers=headers, timeout=10)
        logger.debug("Logout Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None
