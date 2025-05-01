import random
import string


def generate_random_email():
    name = "".join(random.choices(string.ascii_lowercase, k=8))
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com"])
    return f"{name}@{domain}"
