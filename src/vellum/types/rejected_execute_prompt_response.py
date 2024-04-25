# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1
from .prompt_execution_meta import PromptExecutionMeta
from .vellum_error import VellumError


class RejectedExecutePromptResponse(pydantic_v1.BaseModel):
    """
    The unsuccessful response from the model containing an error of what went wrong.
    """

    meta: typing.Optional[PromptExecutionMeta] = None
    raw: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    The subset of the raw response from the model that the request opted into with `expand_raw`.
    """

    execution_id: str = pydantic_v1.Field()
    """
    The ID of the execution.
    """

    error: VellumError

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
