import pytest
from datetime import datetime
import time

from deepdiff import DeepDiff

from tests.workflows.basic_emitter_workflow.workflow import BasicEmitterWorkflow, ExampleEmitter, NextNode, StartNode


@pytest.fixture
def mock_datetime_now(mocker):
    def _mock_datetime_now(frozen_datetime):
        mocker.patch("vellum.workflows.events.types.datetime_now", return_value=frozen_datetime)
        mocker.patch("vellum.workflows.state.base.datetime_now", return_value=frozen_datetime)
        return frozen_datetime

    return _mock_datetime_now


def test_run_workflow__happy_path(mock_uuid4_generator, mock_datetime_now):
    # GIVEN a uuid for our state
    state_id_generator = mock_uuid4_generator("vellum.workflows.state.base.uuid4")
    runner_generator = mock_uuid4_generator("vellum.workflows.runner.runner.uuid4")
    state_id = state_id_generator()
    trace_id = state_id_generator()
    workflow_span_id = state_id_generator()
    start_node_span_id = runner_generator()
    next_node_span_id = runner_generator()

    # AND a workflow that uses a custom event emitter
    emitter = ExampleEmitter()
    workflow = BasicEmitterWorkflow(emitters=[emitter])

    # WHEN the workflow is run
    frozen_datetime = datetime(2024, 1, 1, 12, 0, 0)
    mock_datetime_now(frozen_datetime)
    final_event = workflow.run()

    # AND we wait for the emitter to emit all of the events
    time.sleep(0.01)

    # THEN the emitter should have emitted all of the expected events
    events = list(emitter.events)

    assert len(events) == 6, final_event

    assert events[0].name == "workflow.execution.initiated"
    assert events[0].trace_id == trace_id
    assert events[0].span_id == workflow_span_id
    assert events[0].timestamp == frozen_datetime

    assert events[1].name == "node.execution.initiated"
    assert events[1].node_definition == StartNode

    assert events[2].name == "node.execution.fulfilled"
    assert events[2].node_definition == StartNode
    assert events[2].outputs == {"final_value": "Hello, World!"}

    assert events[3].name == "node.execution.initiated"
    assert events[3].node_definition == NextNode

    assert events[4].name == "node.execution.fulfilled"
    assert events[4].node_definition == NextNode
    assert events[4].outputs == {"final_value": "Score: 13"}

    assert events[5].name == "workflow.execution.fulfilled"
    assert events[5].outputs == {"final_value": "Score: 13"}

    # AND the emitter should have emitted all of the expected state snapshots
    state_snapshots = list(emitter.state_snapshots)

    base_module = ".".join(__name__.split(".")[:-2])

    assert not DeepDiff(
        state_snapshots[0],
        {
            "meta": {
                "id": str(state_id),
                "trace_id": str(trace_id),
                "span_id": str(workflow_span_id),
                "updated_ts": "2024-01-01T12:00:00",
                "is_terminated": False,
                "workflow_inputs": {},
                "external_inputs": {},
                "node_outputs": {},
                "parent": None,
                "node_execution_cache": {
                    "node_execution_ids": {},
                    "node_executions_initiated": {},
                    "dependencies_invoked": {},
                },
            },
            "score": 0,
        },
    )

    assert not DeepDiff(
        state_snapshots[1],
        {
            "meta": {
                "id": str(state_id),
                "trace_id": str(trace_id),
                "span_id": str(workflow_span_id),
                "updated_ts": "2024-01-01T12:00:00",
                "is_terminated": False,
                "workflow_inputs": {},
                "external_inputs": {},
                "node_outputs": {"StartNode.Outputs.final_value": "Hello, World!"},
                "parent": None,
                "node_execution_cache": {
                    "node_execution_ids": {},
                    "node_executions_initiated": {f"{base_module}.workflow.StartNode": [str(start_node_span_id)]},
                    "dependencies_invoked": {},
                },
            },
            "score": 0,
        },
    )

    assert not DeepDiff(
        state_snapshots[2],
        {
            "meta": {
                "id": str(state_id),
                "trace_id": str(trace_id),
                "span_id": str(workflow_span_id),
                "updated_ts": "2024-01-01T12:00:00",
                "is_terminated": False,
                "workflow_inputs": {},
                "external_inputs": {},
                "node_outputs": {
                    "StartNode.Outputs.final_value": "Hello, World!",
                },
                "parent": None,
                "node_execution_cache": {
                    "node_execution_ids": {
                        f"{base_module}.workflow.StartNode": [str(start_node_span_id)],
                    },
                    "node_executions_initiated": {
                        f"{base_module}.workflow.StartNode": [],
                        f"{base_module}.workflow.NextNode": [str(next_node_span_id)],
                    },
                    "dependencies_invoked": {},
                },
            },
            "score": 13,
        },
    )

    assert not DeepDiff(
        state_snapshots[3],
        {
            "meta": {
                "id": str(state_id),
                "trace_id": str(trace_id),
                "span_id": str(workflow_span_id),
                "updated_ts": "2024-01-01T12:00:00",
                "is_terminated": False,
                "workflow_inputs": {},
                "external_inputs": {},
                "node_outputs": {
                    "StartNode.Outputs.final_value": "Hello, World!",
                    "NextNode.Outputs.final_value": "Score: 13",
                },
                "node_execution_cache": {
                    "node_execution_ids": {
                        f"{base_module}.workflow.StartNode": [str(start_node_span_id)],
                    },
                    "node_executions_initiated": {
                        f"{base_module}.workflow.StartNode": [],
                        f"{base_module}.workflow.NextNode": [str(next_node_span_id)],
                    },
                    "dependencies_invoked": {},
                },
                "parent": None,
            },
            "score": 13,
        },
    )

    assert not DeepDiff(
        state_snapshots[4],
        {
            "meta": {
                "id": str(state_id),
                "trace_id": str(trace_id),
                "span_id": str(workflow_span_id),
                "updated_ts": "2024-01-01T12:00:00",
                "is_terminated": True,
                "workflow_inputs": {},
                "external_inputs": {},
                "node_outputs": {
                    "StartNode.Outputs.final_value": "Hello, World!",
                    "NextNode.Outputs.final_value": "Score: 13",
                },
                "node_execution_cache": {
                    "node_execution_ids": {
                        f"{base_module}.workflow.StartNode": [str(start_node_span_id)],
                        f"{base_module}.workflow.NextNode": [str(next_node_span_id)],
                    },
                    "node_executions_initiated": {
                        f"{base_module}.workflow.StartNode": [],
                        f"{base_module}.workflow.NextNode": [],
                    },
                    "dependencies_invoked": {},
                },
                "parent": None,
            },
            "score": 13,
        },
    )

    assert len(state_snapshots) == 5
