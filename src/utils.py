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



def parsePrice(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if not math.isfinite(value) or value < 0:
            return None
        return round(float(value), 2)
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    if normalized == "gratuit":
        return 0
    normalized = normalized.replace("?", "").replace(" ", "")
    if normalized.startswith("-") or not re.fullmatch(r"\d+(?:[.,]\d{1,2})?", normalized):
        return None
    return round(float(normalized.replace(",", ".")), 2)



def groupBy(items, key):
    if items is None or items == []:
        return {}
    if not isinstance(items, list):
        raise ValueError("items must be a list or None")
    grouped = {}
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("each item must be a dictionary")
        value = item.get(key)
        grouped.setdefault(value, []).append(item)
    return grouped
