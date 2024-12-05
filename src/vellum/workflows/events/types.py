from datetime import datetime
from enum import Enum
import json
from uuid import UUID, uuid4
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BeforeValidator, Field

from vellum.core.pydantic_utilities import UniversalBaseModel
from vellum.workflows.state.encoder import DefaultStateEncoder
from vellum.workflows.types.utils import datetime_now


def default_datetime_factory() -> datetime:
    """
    Makes it possible to mock the datetime factory for testing.
    """

    return datetime_now()


excluded_modules = {"typing", "builtins"}


def serialize_type_encoder(obj: type) -> Dict[str, Any]:
    return {
        "name": obj.__name__,
        "module": obj.__module__.split("."),
    }


def default_serializer(obj: Any) -> Any:
    return json.loads(
        json.dumps(
            obj,
            cls=DefaultStateEncoder,
        )
    )


class CodeResourceDefinition(UniversalBaseModel):
    name: str
    module: List[str]


VellumCodeResourceDefinition = Annotated[
    CodeResourceDefinition,
    BeforeValidator(lambda d: (d if type(d) is dict else serialize_type_encoder(d))),
]


class BaseParentContext(UniversalBaseModel):
    span_id: UUID
    parent: Optional["ParentContext"] = None
    type: str


class BaseDeploymentParentContext(BaseParentContext):
    deployment_id: UUID
    deployment_name: str
    deployment_history_item_id: UUID
    release_tag_id: UUID
    release_tag_name: str
    external_id: Optional[str]


class WorkflowDeploymentParentContext(BaseDeploymentParentContext):
    type: Literal["WORKFLOW_RELEASE_TAG"] = "WORKFLOW_RELEASE_TAG"
    workflow_version_id: UUID


class PromptDeploymentParentContext(BaseDeploymentParentContext):
    type: Literal["PROMPT_RELEASE_TAG"] = "PROMPT_RELEASE_TAG"
    prompt_version_id: UUID


class NodeParentContext(BaseParentContext):
    type: Literal["WORKFLOW_NODE"] = "WORKFLOW_NODE"
    node_definition: VellumCodeResourceDefinition


class WorkflowParentContext(BaseParentContext):
    type: Literal["WORKFLOW"] = "WORKFLOW"
    workflow_definition: VellumCodeResourceDefinition


# Define the discriminated union
ParentContext = Annotated[
    Union[
        WorkflowParentContext,
        NodeParentContext,
        WorkflowDeploymentParentContext,
        PromptDeploymentParentContext,
    ],
    Field(discriminator="type"),
]

# Update the forward references
BaseParentContext.model_rebuild()


class BaseEvent(UniversalBaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=default_datetime_factory)
    api_version: Literal["2024-10-25"] = "2024-10-25"
    trace_id: UUID
    span_id: UUID
    parent: Optional[ParentContext] = None
