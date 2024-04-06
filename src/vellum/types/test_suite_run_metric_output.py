# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from .test_suite_run_metric_error_output import TestSuiteRunMetricErrorOutput
from .test_suite_run_metric_number_output import TestSuiteRunMetricNumberOutput


class TestSuiteRunMetricOutput_Number(TestSuiteRunMetricNumberOutput):
    type: typing.Literal["NUMBER"] = "NUMBER"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class TestSuiteRunMetricOutput_Error(TestSuiteRunMetricErrorOutput):
    type: typing.Literal["ERROR"] = "ERROR"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


TestSuiteRunMetricOutput = typing.Union[TestSuiteRunMetricOutput_Number, TestSuiteRunMetricOutput_Error]