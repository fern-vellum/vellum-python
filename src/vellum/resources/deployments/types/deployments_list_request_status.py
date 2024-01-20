# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class DeploymentsListRequestStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

    def visit(self, active: typing.Callable[[], T_Result], archived: typing.Callable[[], T_Result]) -> T_Result:
        if self is DeploymentsListRequestStatus.ACTIVE:
            return active()
        if self is DeploymentsListRequestStatus.ARCHIVED:
            return archived()
