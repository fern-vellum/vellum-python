from uuid import uuid4

from vellum.workflows.events import WorkflowEventType
from vellum.workflows.events.types import NodeParentContext
from vellum_ee.workflows.display.vellum import CodeResourceDefinition

from tests.workflows.basic_parent_context.basic_workflow import TrivialWorkflow


def test_run_workflow__happy_path():
    workflow = TrivialWorkflow()
    terminal_event = workflow.run()

    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.parent == None


def test_stream_workflow__happy_path():
    workflow = TrivialWorkflow()
    events = list(
        workflow.stream(
            event_types={WorkflowEventType.WORKFLOW, WorkflowEventType.NODE}
        )
    )

    assert len(events) == 4

    assert events[0].name == "workflow.execution.initiated"
    assert events[0].parent is None

    assert events[1].name == "node.execution.initiated"
    parent_context = events[1].parent.model_dump() if events[1].parent else {}
    assert parent_context.get("type") == "WORKFLOW"
    assert parent_context.get("parent") is None
    assert parent_context.get("workflow_definition") is not None

    assert events[-1].name == "workflow.execution.fulfilled"
    assert events[-1].parent is None


def test_stream_workflow__happy_path_inital_context():
    initial_parent_context_json = {
        "span_id": uuid4(),
        "node_definition": {
            "module": ["example", "test"],
            "name": "node_workflow",
        },
        "parent": None,
        "type": "WORKFLOW_NODE",
    }
    initial_parent_context = NodeParentContext(**initial_parent_context_json)
    assert type(initial_parent_context.node_definition) == CodeResourceDefinition

    workflow = TrivialWorkflow(parent_context=initial_parent_context)
    events = list(
        workflow.stream(
            event_types={WorkflowEventType.WORKFLOW, WorkflowEventType.NODE}
        )
    )

    assert len(events) == 4

    assert events[0].name == "workflow.execution.initiated"
    assert events[0].parent is not None
    assert events[0].parent == initial_parent_context

    assert events[1].name == "node.execution.initiated"
    parent_context = events[1].parent.model_dump() if events[1].parent else {}
    assert parent_context.get("type") == "WORKFLOW"
    assert parent_context.get("parent") == initial_parent_context_json
    assert parent_context.get("workflow_definition") is not None

    assert events[-1].name == "workflow.execution.fulfilled"
    assert events[-1].parent == initial_parent_context
