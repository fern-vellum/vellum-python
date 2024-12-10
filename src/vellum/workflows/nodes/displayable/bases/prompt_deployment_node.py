from uuid import UUID
from typing import Any, ClassVar, Dict, Generic, Iterator, List, Optional, Sequence, Union, cast

from vellum import (
    ChatHistoryInputRequest,
    ChatMessage,
    ExecutePromptEvent,
    JsonInputRequest,
    PromptDeploymentExpandMetaRequest,
    PromptDeploymentInputRequest,
    RawPromptExecutionOverridesRequest,
    StringInputRequest,
)
from vellum.client import RequestOptions
from vellum.workflows.constants import LATEST_RELEASE_TAG, OMIT
from vellum.workflows.context import get_parent_context
from vellum.workflows.errors import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.displayable.bases.base_prompt_node import BasePromptNode
from vellum.workflows.types.generics import StateType


class BasePromptDeploymentNode(BasePromptNode, Generic[StateType]):
    """
    Used to execute a Prompt Deployment.

    prompt_inputs: EntityInputsInterface - The inputs for the Prompt
    deployment: Union[UUID, str] - Either the Prompt Deployment's UUID or its name.
    release_tag: str - The release tag to use for the Prompt Execution
    external_id: Optional[str] - Optionally include a unique identifier for tracking purposes.
        Must be unique within a given Prompt Deployment.
    expand_meta: Optional[PromptDeploymentExpandMetaRequest] - Expandable execution fields to include in the response
    raw_overrides: Optional[RawPromptExecutionOverridesRequest] - The raw overrides to use for the Prompt Execution
    expand_raw: Optional[Sequence[str]] - Expandable raw fields to include in the response
    metadata: Optional[Dict[str, Optional[Any]]] - The metadata to use for the Prompt Execution
    request_options: Optional[RequestOptions] - The request options to use for the Prompt Execution
    """

    # Either the Prompt Deployment's UUID or its name.
    deployment: ClassVar[Union[UUID, str]]

    release_tag: str = LATEST_RELEASE_TAG
    external_id: Optional[str] = OMIT

    expand_meta: Optional[PromptDeploymentExpandMetaRequest] = OMIT
    raw_overrides: Optional[RawPromptExecutionOverridesRequest] = OMIT
    expand_raw: Optional[Sequence[str]] = OMIT
    metadata: Optional[Dict[str, Optional[Any]]] = OMIT

    def _get_prompt_event_stream(self) -> Iterator[ExecutePromptEvent]:
        current_parent_context = get_parent_context()
        parent_context = current_parent_context.model_dump_json() if current_parent_context else None
        request_options = self.request_options or RequestOptions()
        request_options["additional_body_parameters"] = {
            "execution_context": {"parent_context": parent_context},
            **request_options.get("additional_body_parameters", {}),
        }
        return self._context.vellum_client.execute_prompt_stream(
            inputs=self._compile_prompt_inputs(),
            prompt_deployment_id=str(self.deployment) if isinstance(self.deployment, UUID) else None,
            prompt_deployment_name=self.deployment if isinstance(self.deployment, str) else None,
            release_tag=self.release_tag,
            external_id=self.external_id,
            expand_meta=self.expand_meta,
            raw_overrides=self.raw_overrides,
            expand_raw=self.expand_raw,
            metadata=self.metadata,
            request_options=self.request_options,
        )

    def _compile_prompt_inputs(self) -> List[PromptDeploymentInputRequest]:
        # TODO: We may want to consolidate with subworkflow deployment input compilation
        # https://app.shortcut.com/vellum/story/4117

        compiled_inputs: List[PromptDeploymentInputRequest] = []

        for input_name, input_value in self.prompt_inputs.items():
            if isinstance(input_value, str):
                compiled_inputs.append(
                    StringInputRequest(
                        name=input_name,
                        value=input_value,
                    )
                )
            elif isinstance(input_value, list) and all(isinstance(message, ChatMessage) for message in input_value):
                compiled_inputs.append(
                    ChatHistoryInputRequest(
                        name=input_name,
                        value=cast(List[ChatMessage], input_value),
                    )
                )
            elif isinstance(input_value, dict):
                # Note: We may want to fail early here if we know that input_value is not
                #   JSON serializable.
                compiled_inputs.append(
                    JsonInputRequest(
                        name=input_name,
                        value=cast(Dict[str, Any], input_value),
                    )
                )
            else:
                raise NodeException(
                    message=f"Unrecognized input type for input '{input_name}': {input_value.__class__}",
                    code=VellumErrorCode.INVALID_INPUTS,
                )

        return compiled_inputs
