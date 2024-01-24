# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class WorkflowNodeResultEventState(str, enum.Enum):
    """
    - `INITIATED` - INITIATED
    - `STREAMING` - STREAMING
    - `FULFILLED` - FULFILLED
    - `REJECTED` - REJECTED
    """

    INITIATED = "INITIATED"
    STREAMING = "STREAMING"
    FULFILLED = "FULFILLED"
    REJECTED = "REJECTED"

    def visit(
        self,
        initiated: typing.Callable[[], T_Result],
        streaming: typing.Callable[[], T_Result],
        fulfilled: typing.Callable[[], T_Result],
        rejected: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is WorkflowNodeResultEventState.INITIATED:
            return initiated()
        if self is WorkflowNodeResultEventState.STREAMING:
            return streaming()
        if self is WorkflowNodeResultEventState.FULFILLED:
            return fulfilled()
        if self is WorkflowNodeResultEventState.REJECTED:
            return rejected()