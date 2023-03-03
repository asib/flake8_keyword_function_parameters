import ast
import itertools
import sys
from typing import Any, Generator, List, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


def _arg_is_self(a: ast.arg) -> bool:
    return a.arg == "self"


def _has_positional_self_arg(node: ast.FunctionDef) -> bool:
    return any(
        itertools.chain(
            map(_arg_is_self, node.args.args),
            map(_arg_is_self, node.args.posonlyargs),
        )
    )


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: List[Tuple[int, int]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        positional_args = len(node.args.args) + len(node.args.posonlyargs)

        if positional_args > 1:
            if _has_positional_self_arg(node):
                positional_args -= 1

            if positional_args > 1:
                self.problems.append((node.lineno, node.col_offset))

        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col in visitor.problems:
            yield (
                line,
                col,
                "KFP100 multiple non-keyword arguments in function definition",
                type(self),
            )
