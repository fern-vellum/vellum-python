from vellum.types import CodeExecutionPackage
from vellum.workflows.nodes.displayable import CodeExecutionNode as BaseCodeExecutionNode
from vellum.workflows.state import BaseState

from ..inputs import Inputs


class CodeExecutionNode(BaseCodeExecutionNode[BaseState, str]):
    filepath = "./script.py"
    code_inputs = {"arg": Inputs.input}
    output_type = "STRING"
    runtime = "PYTHON_3_11_6"
    packages = [CodeExecutionPackage(name="requests", version="2.26.0")]
