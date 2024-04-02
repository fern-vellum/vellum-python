# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .test_suite_run_deployment_release_tag_exec_config_request import TestSuiteRunDeploymentReleaseTagExecConfigRequest
from .test_suite_run_workflow_release_tag_exec_config_request import TestSuiteRunWorkflowReleaseTagExecConfigRequest


class TestSuiteRunExecConfigRequest_DeploymentReleaseTag(TestSuiteRunDeploymentReleaseTagExecConfigRequest):
    type: typing_extensions.Literal["DEPLOYMENT_RELEASE_TAG"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class TestSuiteRunExecConfigRequest_WorkflowReleaseTag(TestSuiteRunWorkflowReleaseTagExecConfigRequest):
    type: typing_extensions.Literal["WORKFLOW_RELEASE_TAG"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


TestSuiteRunExecConfigRequest = typing.Union[
    TestSuiteRunExecConfigRequest_DeploymentReleaseTag, TestSuiteRunExecConfigRequest_WorkflowReleaseTag
]
