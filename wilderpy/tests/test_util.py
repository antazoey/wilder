from wilder.util import to_bool
from wilder.util import to_int


def test_to_bool_when_given_none_returns_none():
    assert to_bool(None) is None


def test_to_bool_when_given_true_returns_true():
    assert to_bool(True)


def test_to_bool_when_given_false_returns_false():
    assert not to_bool(False)


def test_to_bool_when_given_true_string_returns_true():
    assert to_bool("true")
    assert to_bool("tRue")
    assert to_bool("TRUE")


def test_to_bool_when_given_t_string_returns_true():
    assert to_bool("t")
    assert to_bool("T")


def test_to_bool_when_given_false_string_returns_false():
    assert not to_bool("false")
    assert not to_bool("falSE")
    assert not to_bool("FALSE")


def test_to_bool_when_given_f_string_returns_false():
    assert not to_bool("f")
    assert not to_bool("F")


def test_to_bool_when_given_random_string_returns_none():
    assert to_bool("truetruetrue") is None


def test_to_bool_when_given_0_returns_false():
    assert not to_bool(0)


def test_to_bool_when_given_1_returns_true():
    assert to_bool(1)


def test_to_bool_when_given_random_int_returns_none():
    assert to_bool(123) is None


def test_to_int_when_given_numeric_str_returns_int():
    assert to_int("45") == 45


def test_to_int_when_given_non_numeric_str_returns_none():
    assert to_int("asdf34") is None


def test_to_int_when_given_none_returns_none():
    assert to_int(None) is None


def test_to_int_when_given_int_returns_int():
    assert to_int(5050) == 5050
