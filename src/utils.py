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



def sortStudents(students, sortBy, order="asc"):
    if not students:
        return []
    if not isinstance(students, list):
        raise ValueError("students must be a list or None")
    if sortBy not in ("name", "grade", "age"):
        raise ValueError("sortBy must be name, grade, or age")
    if order not in ("asc", "desc"):
        raise ValueError("order must be asc or desc")
    return sorted(students, key=lambda student: student[sortBy], reverse=order == "desc")
