import json
import requests
from Tests.config.config_log import logger
from Tests.config.env import Env


def add_contact(token):
    endpoint = "/contacts"
    payload = json.dumps(
        {
            "firstName": "Test",
            "lastName": "Contact",
            "email": "test.contact@example.com",
            "phone": "1234567890",
        }
    )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    try:
        response = requests.post(
            f"{Env.URL}{endpoint}", headers=headers, data=payload, timeout=5
        )
        logger.debug("Contact Created -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def get_contacts(token):
    endpoint = "/contacts"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{Env.URL}{endpoint}", headers=headers, timeout=10)
        logger.debug("Get Contacts Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def get_contact_by_id(token, contact_id):
    endpoint = f"/contacts/{contact_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{Env.URL}{endpoint}", headers=headers, timeout=10)
        logger.debug("Get Contact By ID Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def update_contact(token, contact_id, method="patch", payload=None):
    endpoint = f"/contacts/{contact_id}"
    if payload is None:
        payload = {
            "firstName": "Updated",
            "lastName": "Contact",
            "email": "updated.contact@example.com",
            "phone": "9876543210",
        }

    headers = {
        "Authorization": f"Bearer {token}" if token else "",
        "Content-Type": "application/json",
    }

    try:
        if method.lower() == "put":
            response = requests.put(
                f"{Env.URL}{endpoint}", headers=headers, json=payload, timeout=10
            )
        else:
            response = requests.patch(
                f"{Env.URL}{endpoint}", headers=headers, json=payload, timeout=10
            )
        logger.debug("Update Contact Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def delete_contact(token, contact_id):
    endpoint = f"/contacts/{contact_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.delete(f"{Env.URL}{endpoint}", headers=headers, timeout=10)
        logger.debug("Delete Contact Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None


def add_contact_with_payload(token, payload):
    endpoint = "/contacts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" if token else "",
    }

    try:
        response = requests.post(
            f"{Env.URL}{endpoint}", headers=headers, json=payload, timeout=5
        )
        logger.debug("Custom Contact Creation Response -> %s", response.text)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", e)
        return None
