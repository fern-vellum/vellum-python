import pytest
from uuid import uuid4
from typing import Dict

from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.references.workflow_input import WorkflowInputReference
from vellum.workflows.types.core import JsonObject
from vellum_ee.workflows.display.base import WorkflowInputsDisplayType
from vellum_ee.workflows.display.nodes.get_node_display_class import get_node_display_class
from vellum_ee.workflows.display.nodes.vellum.base_node import BaseNodeDisplay
from vellum_ee.workflows.display.types import WorkflowDisplayContext
from vellum_ee.workflows.display.vellum import NodeDisplayData, WorkflowMetaVellumDisplay
from vellum_ee.workflows.display.workflows.vellum_workflow_display import VellumWorkflowDisplay


@pytest.fixture()
def serialize_node():
    def _serialize_node(
        node_class: BaseNode,
        global_workflow_input_displays: Dict[WorkflowInputReference, WorkflowInputsDisplayType] = {},
    ) -> JsonObject:
        node_display_class = get_node_display_class(BaseNodeDisplay, node_class)
        node_display = node_display_class()

        context: WorkflowDisplayContext = WorkflowDisplayContext(
            workflow_display_class=VellumWorkflowDisplay,
            workflow_display=WorkflowMetaVellumDisplay(
                entrypoint_node_id=uuid4(),
                entrypoint_node_source_handle_id=uuid4(),
                entrypoint_node_display=NodeDisplayData(),
            ),
            node_displays={node_class: node_display},
            global_workflow_input_displays=global_workflow_input_displays,
        )
        return node_display.serialize(context)

    return _serialize_node
