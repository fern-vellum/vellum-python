# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class FunctionDefinitionPromptBlockProperties(UniversalBaseModel):
    function_name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The name identifying the function.
    """

    function_description: typing.Optional[str] = pydantic.Field(default=None)
    """
    A description to help guide the model when to invoke this function.
    """

    function_parameters: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = pydantic.Field(default=None)
    """
    An OpenAPI specification of parameters that are supported by this function.
    """

    function_forced: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Set this option to true to force the model to return a function call of this function.
    """

    function_strict: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Set this option to use strict schema decoding when available.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
