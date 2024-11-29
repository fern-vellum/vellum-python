# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .chat_message_role import ChatMessageRole
from .chat_message_content_request import ChatMessageContentRequest
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ChatMessageRequest(UniversalBaseModel):
    text: typing.Optional[str] = None
    role: ChatMessageRole
    content: typing.Optional[ChatMessageContentRequest] = None
    source: typing.Optional[str] = pydantic.Field(default=None)
    """
    An optional identifier representing who or what generated this message.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow