# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .function_call import FunctionCall
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TerminalNodeFunctionCallResult(UniversalBaseModel):
    id: typing.Optional[str] = None
    name: str = pydantic.Field()
    """
    The unique name given to the terminal node that produced this output.
    """

    type: typing.Literal["FUNCTION_CALL"] = "FUNCTION_CALL"
    value: typing.Optional[FunctionCall] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
