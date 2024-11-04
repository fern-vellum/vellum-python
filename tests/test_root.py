# This file was auto-generated by Fern from our API Definition.

from vellum import Vellum
from vellum import AsyncVellum
import typing
from vellum import StringInputRequest
from vellum import CodeExecutionPackageRequest
from .utilities import validate_response
from vellum import WorkflowRequestStringInputRequest
from vellum import GenerateRequest
from vellum import SubmitCompletionActualRequest
from vellum import WorkflowExecutionActualStringRequest


async def test_execute_code(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {"log": "log", "output": {"type": "STRING", "value": "value"}}
    expected_types: typing.Any = {"log": None, "output": {"type": None, "value": None}}
    response = client.execute_code(
        code="code",
        runtime="PYTHON_3_11_6",
        input_values=[StringInputRequest(name="name", value="value")],
        packages=[CodeExecutionPackageRequest(version="version", name="name")],
        output_type="STRING",
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.execute_code(
        code="code",
        runtime="PYTHON_3_11_6",
        input_values=[StringInputRequest(name="name", value="value")],
        packages=[CodeExecutionPackageRequest(version="version", name="name")],
        output_type="STRING",
    )
    validate_response(async_response, expected_response, expected_types)


async def test_execute_prompt(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "meta": {
            "model_name": "model_name",
            "latency": 1,
            "deployment_release_tag": "deployment_release_tag",
            "prompt_version_id": "prompt_version_id",
            "finish_reason": "LENGTH",
            "usage": {
                "output_token_count": 1,
                "input_token_count": 1,
                "input_char_count": 1,
                "output_char_count": 1,
                "compute_nanos": 1,
                "cache_creation_input_tokens": 1,
                "cache_read_input_tokens": 1,
            },
            "cost": {"value": 1.1, "unit": "USD"},
        },
        "raw": {"key": "value"},
        "execution_id": "execution_id",
        "state": "FULFILLED",
        "outputs": [{"type": "STRING", "value": "value"}],
    }
    expected_types: typing.Any = {
        "meta": {
            "model_name": None,
            "latency": "integer",
            "deployment_release_tag": None,
            "prompt_version_id": None,
            "finish_reason": None,
            "usage": {
                "output_token_count": "integer",
                "input_token_count": "integer",
                "input_char_count": "integer",
                "output_char_count": "integer",
                "compute_nanos": "integer",
                "cache_creation_input_tokens": "integer",
                "cache_read_input_tokens": "integer",
            },
            "cost": {"value": None, "unit": None},
        },
        "raw": ("dict", {0: (None, None)}),
        "execution_id": None,
        "state": None,
        "outputs": ("list", {0: {"type": None, "value": None}}),
    }
    response = client.execute_prompt(inputs=[StringInputRequest(name="name", value="value")])
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.execute_prompt(inputs=[StringInputRequest(name="name", value="value")])
    validate_response(async_response, expected_response, expected_types)


async def test_execute_workflow(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "execution_id": "execution_id",
        "run_id": "run_id",
        "external_id": "external_id",
        "data": {
            "id": "id",
            "state": "FULFILLED",
            "ts": "2024-01-15T09:30:00Z",
            "outputs": [{"id": "id", "name": "name", "type": "STRING"}],
        },
    }
    expected_types: typing.Any = {
        "execution_id": None,
        "run_id": None,
        "external_id": None,
        "data": {
            "id": None,
            "state": None,
            "ts": "datetime",
            "outputs": ("list", {0: {"id": None, "name": None, "type": None}}),
        },
    }
    response = client.execute_workflow(inputs=[WorkflowRequestStringInputRequest(name="name", value="value")])
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.execute_workflow(
        inputs=[WorkflowRequestStringInputRequest(name="name", value="value")]
    )
    validate_response(async_response, expected_response, expected_types)


async def test_generate(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "results": [
            {
                "data": {
                    "completions": [
                        {
                            "id": "id",
                            "text": "text",
                            "prompt_version_id": "prompt_version_id",
                            "deployment_release_tag": "deployment_release_tag",
                            "model_name": "model_name",
                        }
                    ]
                },
                "error": {"message": "message"},
            }
        ]
    }
    expected_types: typing.Any = {
        "results": (
            "list",
            {
                0: {
                    "data": {
                        "completions": (
                            "list",
                            {
                                0: {
                                    "id": None,
                                    "text": None,
                                    "prompt_version_id": None,
                                    "deployment_release_tag": None,
                                    "model_name": None,
                                }
                            },
                        )
                    },
                    "error": {"message": None},
                }
            },
        )
    }
    response = client.generate(requests=[GenerateRequest(input_values={"key": "value"})])
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.generate(requests=[GenerateRequest(input_values={"key": "value"})])
    validate_response(async_response, expected_response, expected_types)


async def test_search(client: Vellum, async_client: AsyncVellum) -> None:
    expected_response: typing.Any = {
        "results": [{"text": "text", "score": 1.1, "keywords": ["keywords"], "document": {"label": "label"}}]
    }
    expected_types: typing.Any = {
        "results": (
            "list",
            {0: {"text": None, "score": None, "keywords": ("list", {0: None}), "document": {"label": None}}},
        )
    }
    response = client.search(query="query")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.search(query="query")
    validate_response(async_response, expected_response, expected_types)


async def test_submit_completion_actuals(client: Vellum, async_client: AsyncVellum) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.submit_completion_actuals(actuals=[SubmitCompletionActualRequest()])  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.submit_completion_actuals(actuals=[SubmitCompletionActualRequest()])  # type: ignore[func-returns-value]
        is None
    )


async def test_submit_workflow_execution_actuals(client: Vellum, async_client: AsyncVellum) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.submit_workflow_execution_actuals(actuals=[WorkflowExecutionActualStringRequest()])  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.submit_workflow_execution_actuals(actuals=[WorkflowExecutionActualStringRequest()])  # type: ignore[func-returns-value]
        is None
    )
