import ast
from typing import Set

from precisely import assert_that, equal_to

from flake8_keyword_function_parameters import Plugin

_WARNING = "KFP100 multiple non-keyword arguments in function definition"


def _multiple_non_keyword_args(line: int, col: int):
    return f"{line}:{col} {_WARNING}"


def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert_that(_results(""), equal_to(set()))


def test_single_positional_argument_is_allowed():
    s = "def f(a): pass"

    assert_that(_results(s), equal_to(set()))


def test_multiple_non_keyword_arguments_are_rejected():
    s = "def f(a, b): pass"

    assert_that(_results(s), equal_to({_multiple_non_keyword_args(1, 1)}))


def test_single_positional_argument_with_keyword_only_arguments_allowed():
    s = "def f(a, *, b, c): pass"

    assert_that(_results(s), equal_to(set()))


def test_multiple_positional_args_with_keyword_only_arguments_rejected():
    s = "def f(a, b, *, c, d): pass"

    assert_that(_results(s), equal_to({_multiple_non_keyword_args(1, 1)}))


def test_multiple_keyword_arguments_are_allowed():
    s = "def f(*, a, b): pass"

    assert_that(_results(s), equal_to(set()))


def test_positional_self_arg_and_one_other_positional_arg_is_allowed():
    s = """
class A:
    def a(self, b): pass
"""

    assert_that(_results(s), equal_to(set()))


def test_positional_self_arg_and_multiple_other_positional_args_are_rejected():
    s = """
class A:
    def a(self, b, c): pass
"""

    assert_that(_results(s), equal_to({_multiple_non_keyword_args(3, 5)}))
