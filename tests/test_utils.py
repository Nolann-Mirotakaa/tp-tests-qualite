from src.utils import calculateAverage, capitalize, clamp, slugify


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
