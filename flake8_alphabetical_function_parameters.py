import ast
import sys
from typing import Generator, Tuple, Type, Any

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: List[Tuple[int, int]] = []
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if (
            len(node.args.args) > 1
            or (len(node.args.args) == 1 and len(node.args.kwonlyargs) != 0)
        ):
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
            yield line, col, 'AFP100 multiple non-keyword arguments in function definition', type(self)