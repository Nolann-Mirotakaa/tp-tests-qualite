import math
import re
import unicodedata


def capitalize(value):
    if not isinstance(value, str) or not value:
        return ""
    return value[0].upper() + value[1:].lower()


def calculateAverage(numbers):
    if not isinstance(numbers, (list, tuple)) or not numbers:
        return 0
    if any(isinstance(item, bool) or not isinstance(item, (int, float)) for item in numbers):
        return 0
    if any(not math.isfinite(item) for item in numbers):
        return 0
    return round(sum(numbers) / len(numbers), 2)


def slugify(text):
    if not isinstance(text, str):
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    ascii_text = re.sub(r"[^a-z0-9\s-]", "", ascii_text)
    return re.sub(r"[\s-]+", "-", ascii_text).strip("-")


def clamp(value, minimum, maximum):
    if minimum > maximum:
        raise ValueError("minimum must be less than or equal to maximum")
    return max(minimum, min(value, maximum))
