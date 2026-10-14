from src.utils import calculateAverage, capitalize, clamp, slugify, sortStudents, parsePrice, groupBy


def test_capitalize_lowercase_word():
    assert capitalize("hello") == "Hello"


def test_capitalize_uppercase_word():
    assert capitalize("WORLD") == "World"


def test_capitalize_empty_string():
    assert capitalize("") == ""


def test_capitalize_none():
    assert capitalize(None) == ""


def test_average_three_values():
    assert calculateAverage([10, 12, 14]) == 12


def test_average_single_value():
    assert calculateAverage([15]) == 15


def test_average_empty_list():
    assert calculateAverage([]) == 0


def test_average_rounds_to_two_decimals():
    assert calculateAverage([10, 11, 12]) == 11


def test_average_none():
    assert calculateAverage(None) == 0


def test_slugify_simple_words():
    assert slugify("Hello World") == "hello-world"


def test_slugify_trims_surrounding_spaces():
    assert slugify(" Spaces Everywhere ") == "spaces-everywhere"


def test_slugify_removes_apostrophes_and_punctuation():
    assert slugify("C'est l'ete !") == "cest-lete"


def test_slugify_empty_string():
    assert slugify("") == ""


def test_slugify_none():
    assert slugify(None) == ""


def test_clamp_keeps_value_inside_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_uses_minimum_for_low_value():
    assert clamp(-5, 0, 10) == 0


def test_clamp_uses_maximum_for_high_value():
    assert clamp(15, 0, 10) == 10


def test_clamp_supports_equal_bounds():
    assert clamp(0, 0, 0) == 0



def student_sample():
    return [
        {"name": "Charlie", "grade": 70, "age": 22},
        {"name": "Alice", "grade": 90, "age": 20},
        {"name": "Bob", "grade": 80, "age": 21},
    ]


def test_sort_students_by_grade_ascending():
    assert [s["grade"] for s in sortStudents(student_sample(), "grade")] == [70, 80, 90]


def test_sort_students_by_grade_descending():
    assert [s["grade"] for s in sortStudents(student_sample(), "grade", "desc")] == [90, 80, 70]


def test_sort_students_by_name_ascending():
    assert [s["name"] for s in sortStudents(student_sample(), "name")] == ["Alice", "Bob", "Charlie"]


def test_sort_students_by_age_ascending():
    assert [s["age"] for s in sortStudents(student_sample(), "age")] == [20, 21, 22]


def test_sort_students_returns_empty_list_for_none():
    assert sortStudents(None, "grade") == []


def test_sort_students_returns_empty_list_for_empty_list():
    assert sortStudents([], "grade") == []


def test_sort_students_does_not_mutate_input():
    original = student_sample()
    snapshot = [student.copy() for student in original]
    sortStudents(original, "name")
    assert original == snapshot


def test_sort_students_defaults_to_ascending_order():
    assert [s["grade"] for s in sortStudents(student_sample(), "grade")] == [70, 80, 90]




def test_parse_price_from_dot_decimal():
    assert parsePrice("12.99") == 12.99


def test_parse_price_from_comma_decimal():
    assert parsePrice("12,99") == 12.99


def test_parse_price_with_currency_suffix():
    assert parsePrice("12.99 ?") == 12.99


def test_parse_price_with_currency_prefix():
    assert parsePrice("?12.99") == 12.99


def test_parse_price_from_number():
    assert parsePrice(12.99) == 12.99


def test_parse_price_from_gratuit():
    assert parsePrice("gratuit") == 0


def test_parse_price_rejects_invalid_text():
    assert parsePrice("abc") is None


def test_parse_price_rejects_negative_amount():
    assert parsePrice("-5.00") is None


def test_parse_price_rejects_none():
    assert parsePrice(None) is None



def test_group_by_creates_multiple_groups():
    people = [{"name": "Alice", "role": "dev"}, {"name": "Bob", "role": "design"}, {"name": "Charlie", "role": "dev"}]
    result = groupBy(people, "role")
    assert [person["name"] for person in result["dev"]] == ["Alice", "Charlie"]
    assert [person["name"] for person in result["design"]] == ["Bob"]


def test_group_by_returns_empty_dict_for_empty_input():
    assert groupBy([], "role") == {}


def test_group_by_returns_empty_dict_for_none():
    assert groupBy(None, "role") == {}


def test_group_by_supports_a_single_group():
    assert groupBy([{"role": "dev"}], "role") == {"dev": [{"role": "dev"}]}


def test_group_by_puts_missing_keys_in_none_group():
    assert groupBy([{"name": "Alice"}], "role") == {None: [{"name": "Alice"}]}
