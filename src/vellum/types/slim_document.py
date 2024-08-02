# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .document_document_to_document_index import DocumentDocumentToDocumentIndex
from .document_status import DocumentStatus
from .processing_failure_reason_enum import ProcessingFailureReasonEnum
from .processing_state_enum import ProcessingStateEnum


class SlimDocument(pydantic_v1.BaseModel):
    id: str = pydantic_v1.Field()
    """
    Vellum-generated ID that uniquely identifies this document.
    """

    external_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The external ID that was originally provided when uploading the document.
    """

    last_uploaded_at: dt.datetime = pydantic_v1.Field()
    """
    A timestamp representing when this document was most recently uploaded.
    """

    label: str = pydantic_v1.Field()
    """
    Human-friendly name for this document.
    """

    processing_state: typing.Optional[ProcessingStateEnum] = pydantic_v1.Field(default=None)
    """
    An enum value representing where this document is along its processing lifecycle. Note that this is different than its indexing lifecycle.
    
    - `QUEUED` - Queued
    - `PROCESSING` - Processing
    - `PROCESSED` - Processed
    - `FAILED` - Failed
    """

    processing_failure_reason: typing.Optional[ProcessingFailureReasonEnum] = pydantic_v1.Field(default=None)
    """
    An enum value representing why the document could not be processed. Is null unless processing_state is FAILED.
    
    - `EXCEEDED_CHARACTER_LIMIT` - Exceeded Character Limit
    - `INVALID_FILE` - Invalid File
    """

    status: typing.Optional[DocumentStatus] = pydantic_v1.Field(default=None)
    """
    The document's current status.
    
    - `ACTIVE` - Active
    """

    keywords: typing.Optional[typing.List[str]] = pydantic_v1.Field(default=None)
    """
    A list of keywords associated with this document. Originally provided when uploading the document.
    """

    metadata: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    A previously supplied JSON object containing metadata that can be filtered on when searching.
    """

    document_to_document_indexes: typing.List[DocumentDocumentToDocumentIndex]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
