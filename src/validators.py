import re


_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_SPECIAL_CHARACTERS = set("!@#$%^&*")


def isValidEmail(email):
    return isinstance(email, str) and _EMAIL_PATTERN.fullmatch(email) is not None


def isValidPassword(password):
    if not isinstance(password, str):
        password = ""
    errors = []
    if len(password) < 8:
        errors.append("minimum 8 characters")
    if not any(character.isupper() for character in password):
        errors.append("at least one uppercase letter")
    if not any(character.islower() for character in password):
        errors.append("at least one lowercase letter")
    if not any(character.isdigit() for character in password):
        errors.append("at least one digit")
    if not any(character in _SPECIAL_CHARACTERS for character in password):
        errors.append("at least one special character")
    return {"valid": not errors, "errors": errors}


def isValidAge(age):
    return isinstance(age, int) and not isinstance(age, bool) and 0 <= age <= 150
