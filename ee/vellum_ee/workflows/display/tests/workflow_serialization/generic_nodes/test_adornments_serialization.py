from uuid import uuid4

from deepdiff import DeepDiff

from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.core.retry_node.node import RetryNode
from vellum.workflows.nodes.core.try_node.node import TryNode
from vellum.workflows.outputs.base import BaseOutputs
from vellum_ee.workflows.display.base import WorkflowInputsDisplay
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.nodes.vellum.base_node import BaseNodeDisplay


class Inputs(BaseInputs):
    input: str


@RetryNode.wrap(max_attempts=3)
class InnerRetryGenericNode(BaseNode):
    input = Inputs.input

    class Outputs(BaseOutputs):
        output: str


class InnerRetryGenericNodeDisplay(BaseNodeDisplay[InnerRetryGenericNode.__wrapped_node__]):  # type: ignore
    pass


class OuterRetryNodeDisplay(BaseNodeDisplay[InnerRetryGenericNode]):
    pass


def test_serialize_node__retry(serialize_node):
    input_id = uuid4()
    serialized_node = serialize_node(
        node_class=InnerRetryGenericNode,
        global_workflow_input_displays={Inputs.input: WorkflowInputsDisplay(id=input_id)},
        global_node_displays={
            InnerRetryGenericNode.__wrapped_node__: InnerRetryGenericNodeDisplay,
            InnerRetryGenericNode: OuterRetryNodeDisplay,
        },
    )

    assert not DeepDiff(
        {
            "id": "f2a95e79-7d4b-47ad-b986-4f648297ec65",
            "label": "InnerRetryGenericNode",
            "type": "GENERIC",
            "display_data": {"position": {"x": 0.0, "y": 0.0}},
            "base": {"name": "BaseNode", "module": ["vellum", "workflows", "nodes", "bases", "base"]},
            "definition": {
                "name": "InnerRetryGenericNode",
                "module": [
                    "vellum_ee",
                    "workflows",
                    "display",
                    "tests",
                    "workflow_serialization",
                    "generic_nodes",
                    "test_adornments_serialization",
                ],
            },
            "trigger": {"id": "af9ba01c-4cde-4632-9aa1-7673b42e7bd8", "merge_behavior": "AWAIT_ATTRIBUTES"},
            "ports": [{"id": "55d46900-e558-4264-8802-a5c5fe7226fe", "name": "default", "type": "DEFAULT"}],
            "adornments": [
                {
                    "id": "5be7d260-74f7-4734-b31b-a46a94539586",
                    "label": "RetryNode",
                    "base": {
                        "name": "RetryNode",
                        "module": ["vellum", "workflows", "nodes", "core", "retry_node", "node"],
                    },
                    "attributes": [
                        {
                            "id": "f388e93b-8c68-4f54-8577-bbd0c9091557",
                            "name": "max_attempts",
                            "value": {"type": "CONSTANT_VALUE", "value": {"type": "NUMBER", "value": 3.0}},
                        },
                        {
                            "id": "c91782e3-140f-4938-9c23-d2a7b85dcdd8",
                            "name": "retry_on_error_code",
                            "value": {"type": "CONSTANT_VALUE", "value": {"type": "JSON", "value": None}},
                        },
                        {
                            "id": "73a02e62-4535-4e1f-97b5-1264ca8b1d71",
                            "name": "retry_on_condition",
                            "value": {"type": "CONSTANT_VALUE", "value": {"type": "JSON", "value": None}},
                        },
                    ],
                }
            ],
            "attributes": [
                {
                    "id": "c363daa7-9482-4c0e-aee8-faa080602ee3",
                    "name": "input",
                    "value": {"type": "WORKFLOW_INPUT", "input_variable_id": str(input_id)},
                }
            ],
            "outputs": [
                {"id": "8aaf6cd8-3fa5-4f17-a60f-ec7da5ec6498", "name": "output", "type": "STRING", "value": None}
            ],
        },
        serialized_node,
        ignore_order=True,
    )


@TryNode.wrap()
class InnerTryGenericNode(BaseNode):
    input = Inputs.input

    class Outputs(BaseOutputs):
        output: str


class InnerTryGenericNodeDisplay(BaseNodeDisplay[InnerTryGenericNode.__wrapped_node__]):  # type: ignore
    pass


def test_serialize_node__try(serialize_node):
    input_id = uuid4()
    serialized_node = serialize_node(
        base_class=BaseNodeVellumDisplay,
        node_class=InnerTryGenericNode,
        global_workflow_input_displays={Inputs.input: WorkflowInputsDisplay(id=input_id)},
        global_node_displays={
            InnerTryGenericNode.__wrapped_node__: InnerTryGenericNodeDisplay,
        },
    )

    assert not DeepDiff(
        {
            "id": "f20d49eb-299f-481d-90db-bfa9d1e9d3de",
            "label": "InnerTryGenericNode",
            "type": "GENERIC",
            "display_data": {"position": {"x": 0.0, "y": 0.0}},
            "base": {"name": "BaseNode", "module": ["vellum", "workflows", "nodes", "bases", "base"]},
            "definition": {
                "name": "InnerTryGenericNode",
                "module": [
                    "vellum_ee",
                    "workflows",
                    "display",
                    "tests",
                    "workflow_serialization",
                    "generic_nodes",
                    "test_adornments_serialization",
                ],
            },
            "trigger": {"id": "741f7f75-e921-47a9-8c05-9e66640d0866", "merge_behavior": "AWAIT_ATTRIBUTES"},
            "ports": [{"id": "f76a0b36-018b-4c5c-aa60-102570e2fd8c", "name": "default", "type": "DEFAULT"}],
            "adornments": [
                {
                    "id": "3344083c-a32c-4a32-920b-0fb5093448fa",
                    "label": "TryNode",
                    "base": {"name": "TryNode", "module": ["vellum", "workflows", "nodes", "core", "try_node", "node"]},
                    "attributes": [
                        {
                            "id": "ab2fbab0-e2a0-419b-b1ef-ce11ecf11e90",
                            "name": "on_error_code",
                            "value": {"type": "CONSTANT_VALUE", "value": {"type": "JSON", "value": None}},
                        }
                    ],
                }
            ],
            "attributes": [
                {
                    "id": "4d8b4c2c-4f92-4c7a-abf0-b9c88a15a790",
                    "name": "input",
                    "value": {"type": "WORKFLOW_INPUT", "input_variable_id": str(input_id)},
                }
            ],
            "outputs": [
                {"id": "63ba929b-bf79-44ee-bd1f-d259dbe8d48e", "name": "output", "type": "STRING", "value": None}
            ],
        },
        serialized_node,
        ignore_order=True,
    )
