# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .test_suite_run_deployment_release_tag_exec_config_data_request import (
    TestSuiteRunDeploymentReleaseTagExecConfigDataRequest,
)

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class TestSuiteRunDeploymentReleaseTagExecConfigRequest(pydantic.BaseModel):
    """
    Execution configuration for running a Test Suite against a Prompt Deployment
    """

    data: TestSuiteRunDeploymentReleaseTagExecConfigDataRequest
    test_case_ids: typing.Optional[typing.List[str]] = pydantic.Field(
        description="Optionally specify a subset of test case ids to run. If not provided, all test cases within the test suite will be run by default."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
