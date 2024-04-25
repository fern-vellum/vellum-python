# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1
from .test_suite_run_external_exec_config_data import TestSuiteRunExternalExecConfigData


class TestSuiteRunExternalExecConfig(pydantic_v1.BaseModel):
    """
    Execution configuration for running a Vellum Test Suite against an external callable
    """

    data: TestSuiteRunExternalExecConfigData
    test_case_ids: typing.Optional[typing.List[str]] = pydantic_v1.Field(default=None)
    """
    Optionally specify a subset of test case ids to run. If not provided, all test cases within the test suite will be run by default.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
