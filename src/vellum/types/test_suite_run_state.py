# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class TestSuiteRunState(str, enum.Enum):
    """
    - `QUEUED` - Queued
    - `RUNNING` - Running
    - `COMPLETE` - Complete
    - `FAILED` - Failed
    - `CANCELLED` - Cancelled
    """

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    def visit(
        self,
        queued: typing.Callable[[], T_Result],
        running: typing.Callable[[], T_Result],
        complete: typing.Callable[[], T_Result],
        failed: typing.Callable[[], T_Result],
        cancelled: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is TestSuiteRunState.QUEUED:
            return queued()
        if self is TestSuiteRunState.RUNNING:
            return running()
        if self is TestSuiteRunState.COMPLETE:
            return complete()
        if self is TestSuiteRunState.FAILED:
            return failed()
        if self is TestSuiteRunState.CANCELLED:
            return cancelled()
