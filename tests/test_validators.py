from src.validators import isValidAge, isValidEmail, isValidPassword


def test_email_accepts_basic_address():
    assert isValidEmail("user@example.com") is True


def test_email_accepts_plus_tag_address():
    assert isValidEmail("user.name+tag@domain.co") is True


def test_email_rejects_missing_at_sign():
    assert isValidEmail("invalid") is False


def test_email_rejects_empty_local_part():
    assert isValidEmail("@domain.com") is False


def test_email_rejects_missing_domain():
    assert isValidEmail("user@") is False


def test_email_rejects_empty_string():
    assert isValidEmail("") is False


def test_email_rejects_none():
    assert isValidEmail(None) is False


def test_password_accepts_all_required_character_types():
    assert isValidPassword("Passw0rd!") == {"valid": True, "errors": []}


def test_password_reports_every_error_for_short_password():
    result = isValidPassword("short")
    assert result["valid"] is False
    assert result["errors"] == [
        "minimum 8 characters",
        "at least one uppercase letter",
        "at least one digit",
        "at least one special character",
    ]


def test_password_reports_missing_uppercase():
    assert "at least one uppercase letter" in isValidPassword("alllowercase1!")["errors"]


def test_password_reports_missing_lowercase():
    assert "at least one lowercase letter" in isValidPassword("ALLUPPERCASE1!")["errors"]


def test_password_reports_missing_digit():
    assert "at least one digit" in isValidPassword("NoDigits!here")["errors"]


def test_password_reports_missing_special_character():
    assert "at least one special character" in isValidPassword("NoSpecial1here")["errors"]


def test_password_rejects_empty_string():
    assert isValidPassword("")["valid"] is False


def test_password_rejects_none():
    assert isValidPassword(None)["valid"] is False


def test_age_accepts_typical_integer():
    assert isValidAge(25) is True


def test_age_accepts_zero():
    assert isValidAge(0) is True


def test_age_accepts_maximum():
    assert isValidAge(150) is True


def test_age_rejects_negative_value():
    assert isValidAge(-1) is False


def test_age_rejects_value_above_maximum():
    assert isValidAge(151) is False


def test_age_rejects_float():
    assert isValidAge(25.5) is False


def test_age_rejects_numeric_string():
    assert isValidAge("25") is False


def test_age_rejects_none():
    assert isValidAge(None) is False
