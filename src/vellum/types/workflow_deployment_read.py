# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1
from .entity_status import EntityStatus
from .environment_enum import EnvironmentEnum
from .vellum_variable import VellumVariable


class WorkflowDeploymentRead(pydantic_v1.BaseModel):
    id: str
    name: str = pydantic_v1.Field()
    """
    A name that uniquely identifies this workflow deployment within its workspace
    """

    label: str = pydantic_v1.Field()
    """
    A human-readable label for the workflow deployment
    """

    status: typing.Optional[EntityStatus] = pydantic_v1.Field(default=None)
    """
    The current status of the workflow deployment
    
    - `ACTIVE` - Active
    - `ARCHIVED` - Archived
    """

    environment: typing.Optional[EnvironmentEnum] = pydantic_v1.Field(default=None)
    """
    The environment this workflow deployment is used in
    
    - `DEVELOPMENT` - Development
    - `STAGING` - Staging
    - `PRODUCTION` - Production
    """

    created: dt.datetime
    last_deployed_on: dt.datetime
    input_variables: typing.List[VellumVariable] = pydantic_v1.Field()
    """
    The input variables this Workflow Deployment expects to receive values for when it is executed.
    """

    output_variables: typing.List[VellumVariable] = pydantic_v1.Field()
    """
    The output variables this Workflow Deployment produces values for when it's executed.
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
