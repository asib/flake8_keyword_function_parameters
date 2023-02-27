import ast
from typing import Set

from flake8_alphabetical_function_parameters import Plugin
    
def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = Plugin(tree)
    return {
        f"{line}:{col + 1} {msg}" for line, col, msg, _ in plugin.run()
    }

def test_trivial_case():
    assert _results('') == set()

def test_single_positional_argument_is_allowed():
    s = "def f(a): pass"
    
    assert _results(s) == set()

def test_multiple_non_keyword_arguments_are_rejected():
    s = "def f(a, b): pass"
    
    assert _results(s) == {"1:1 AFP100 multiple non-keyword arguments in function definition"}

def test_multiple_mixed_arguments_are_rejected():
    s = "def f(a, *, b, c): pass"
    
    assert _results(s) == {"1:1 AFP100 multiple non-keyword arguments in function definition"}

def test_multiple_keyword_arguments_are_allowed():
    s = "def f(*, a, b): pass"
    
    assert _results(s) == set()