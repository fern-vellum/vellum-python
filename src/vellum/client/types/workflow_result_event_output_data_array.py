# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_variable_value import ArrayVariableValue
import typing
from .workflow_node_result_event_state import WorkflowNodeResultEventState
import pydantic
from .array_variable_value_item import ArrayVariableValueItem
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.pydantic_utilities import update_forward_refs


class WorkflowResultEventOutputDataArray(UniversalBaseModel):
    """
    An Array output returned from a Workflow execution.
    """

    id: typing.Optional[str] = None
    name: str
    state: WorkflowNodeResultEventState
    node_id: str
    delta: typing.Optional[str] = pydantic.Field(default=None)
    """
    The newly output string value. Only relevant for string outputs with a state of STREAMING.
    """

    type: typing.Literal["ARRAY"] = "ARRAY"
    value: typing.Optional[typing.List[ArrayVariableValueItem]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVariableValue, WorkflowResultEventOutputDataArray=WorkflowResultEventOutputDataArray)