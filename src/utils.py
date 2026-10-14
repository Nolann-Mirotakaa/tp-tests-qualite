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



def calculateDiscount(price, discountRules):
    if isinstance(price, bool) or not isinstance(price, (int, float)) or not math.isfinite(price) or price < 0:
        raise ValueError("price must be a finite non-negative number")
    if not isinstance(discountRules, list):
        raise ValueError("discountRules must be a list")
    remaining = float(price)
    for rule in discountRules:
        if not isinstance(rule, dict):
            raise ValueError("each discount rule must be a dictionary")
        rule_type = rule.get("type")
        value = rule.get("value")
        if rule_type == "percentage":
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError("percentage value must be non-negative")
            remaining *= max(0, 1 - value / 100)
        elif rule_type == "fixed":
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError("fixed value must be non-negative")
            remaining -= value
        elif rule_type == "buyXgetY":
            buy = rule.get("buy")
            free = rule.get("free")
            item_price = rule.get("itemPrice")
            if not all(isinstance(number, int) and not isinstance(number, bool) and number > 0 for number in (buy, free)):
                raise ValueError("buy and free must be positive integers")
            if isinstance(item_price, bool) or not isinstance(item_price, (int, float)) or item_price <= 0:
                raise ValueError("itemPrice must be positive")
            item_count = int(remaining // item_price)
            free_count = item_count // (buy + free) * free
            remaining -= free_count * item_price
        else:
            raise ValueError("unknown discount rule")
        remaining = max(0, remaining)
    return round(remaining, 2)
