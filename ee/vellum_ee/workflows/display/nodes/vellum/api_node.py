from uuid import UUID
from typing import Any, ClassVar, Dict, Generic, Optional, TypeVar, cast

from vellum.workflows.nodes.displayable import APINode
from vellum.workflows.references.output import OutputReference
from vellum.workflows.types.core import JsonArray, JsonObject
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.nodes.utils import raise_if_descriptor
from vellum_ee.workflows.display.nodes.vellum.utils import create_node_input
from vellum_ee.workflows.display.types import WorkflowDisplayContext
from vellum_ee.workflows.display.vellum import ConstantValuePointer, StringVellumValue

_APINodeType = TypeVar("_APINodeType", bound=APINode)


class BaseAPINodeDisplay(BaseNodeVellumDisplay[_APINodeType], Generic[_APINodeType]):
    url_input_id: ClassVar[Optional[UUID]] = None
    method_input_id: ClassVar[Optional[UUID]] = None
    body_input_id: ClassVar[Optional[UUID]] = None

    authorization_type_input_id: ClassVar[Optional[UUID]] = None
    bearer_token_value_input_id: ClassVar[Optional[UUID]] = None
    api_key_header_key_input_id: ClassVar[Optional[UUID]] = None
    api_key_header_value_input_id: ClassVar[Optional[UUID]] = None

    # A mapping between node input keys and their ids for inputs representing additional header keys
    additional_header_key_input_ids: ClassVar[Optional[Dict[str, UUID]]] = None

    # A mapping between node input keys and their ids for inputs representing additional header values
    additional_header_value_input_ids: ClassVar[Optional[Dict[str, UUID]]] = None

    def serialize(
        self, display_context: WorkflowDisplayContext, error_output_id: Optional[UUID] = None, **kwargs: Any
    ) -> JsonObject:
        node = self._node
        node_id = self.node_id

        node_url = raise_if_descriptor(node.url)
        url_node_input = create_node_input(
            node_id=node_id,
            input_name="url",
            value=node_url,
            display_context=display_context,
            input_id=self.url_input_id,
        )

        node_method = raise_if_descriptor(node.method)
        method_node_input = create_node_input(
            node_id=node_id,
            input_name="method",
            value=node_method,
            display_context=display_context,
            input_id=self.method_input_id,
        )

        node_data = raise_if_descriptor(node.data)
        node_json = raise_if_descriptor(node.json)
        body_node_input = create_node_input(
            node_id=node_id,
            input_name="body",
            value=node_data if node_data else node_json,
            display_context=display_context,
            input_id=self.body_input_id,
        )

        headers = raise_if_descriptor(node.headers)
        api_key_header_key = raise_if_descriptor(node.api_key_header_key)
        api_key_header_value = raise_if_descriptor(node.api_key_header_value)
        authorization_type = raise_if_descriptor(node.authorization_type)
        bearer_token_value = raise_if_descriptor(node.bearer_token_value)

        authorization_type_node_input = (
            create_node_input(
                node_id=node_id,
                input_name="authorization_type",
                value=authorization_type,
                display_context=display_context,
                input_id=self.authorization_type_input_id,
            )
            if authorization_type
            else None
        )
        bearer_token_value_node_input = (
            create_node_input(
                node_id=node_id,
                input_name="bearer_token_value",
                value=bearer_token_value,
                display_context=display_context,
                input_id=self.bearer_token_value_input_id,
            )
            if bearer_token_value
            else None
        )
        api_key_header_key_node_input = (
            create_node_input(
                node_id=node_id,
                input_name="api_key_header_key",
                value=api_key_header_key,
                display_context=display_context,
                input_id=self.api_key_header_key_input_id,
            )
            if api_key_header_key
            else None
        )
        api_key_header_value_node_input = (
            create_node_input(
                node_id=node_id,
                input_name="api_key_header_value",
                value=node.api_key_header_value,
                display_context=display_context,
                input_id=self.api_key_header_value_input_id,
            )
            if headers and api_key_header_key and api_key_header_value
            else None
        )

        # TODO: Add stable IDs for additional headers
        # https://app.shortcut.com/vellum/story/5083
        additional_headers: JsonArray = (
            [
                {
                    "header_key_input_id": create_node_input(
                        node_id=node_id,
                        input_name="additional_header_key",
                        value=key,
                        display_context=display_context,
                        input_id=(
                            self.additional_header_key_input_ids.get(key)
                            if self.additional_header_key_input_ids
                            else None
                        ),
                    ).id,
                    "header_value_input_id": create_node_input(
                        node_id=node_id,
                        input_name="additional_header_value",
                        value=value,
                        display_context=display_context,
                        input_id=(
                            self.additional_header_value_input_ids.get(key)
                            if self.additional_header_value_input_ids
                            else None
                        ),
                    ).id,
                }
                for key, value in headers.items()
                if key not in {api_key_header_key, "Authorization"}
            ]
            if headers
            else []
        )

        inputs = [
            input
            for input in [
                url_node_input,
                method_node_input,
                body_node_input,
                authorization_type_node_input,
                bearer_token_value_node_input,
                api_key_header_key_node_input,
                api_key_header_value_node_input,
            ]
            if input is not None
        ]

        _, text_output_display = display_context.node_output_displays[cast(OutputReference, node.Outputs.text)]
        _, json_output_display = display_context.node_output_displays[cast(OutputReference, node.Outputs.json)]
        _, status_code_output_display = display_context.node_output_displays[
            cast(OutputReference, node.Outputs.status_code)
        ]

        return {
            "id": str(node_id),
            "type": "API",
            "inputs": [input.dict() for input in inputs],
            "data": {
                "label": self.label,
                "error_output_id": str(error_output_id) if error_output_id else None,
                "source_handle_id": str(self.get_source_handle_id(display_context.port_displays)),
                "target_handle_id": str(self.get_target_handle_id()),
                "url_input_id": url_node_input.id,
                "method_input_id": method_node_input.id,
                "body_input_id": body_node_input.id,
                "authorization_type_input_id": (
                    authorization_type_node_input.id if authorization_type_node_input else None
                ),
                "bearer_token_value_input_id": (
                    bearer_token_value_node_input.id if bearer_token_value_node_input else None
                ),
                "api_key_header_key_input_id": (
                    api_key_header_key_node_input.id if api_key_header_key_node_input else None
                ),
                "api_key_header_value_input_id": (
                    api_key_header_value_node_input.id if api_key_header_value_node_input else None
                ),
                "additional_headers": additional_headers,
                "text_output_id": str(text_output_display.id),
                "json_output_id": str(json_output_display.id),
                "status_code_output_id": str(status_code_output_display.id),
            },
            "display_data": self.get_display_data().dict(),
            "definition": self.get_definition().dict(),
        }
