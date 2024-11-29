# This file was auto-generated by Fern from our API Definition.

import typing
from .node_input_compiled_string_value import NodeInputCompiledStringValue
from .node_input_compiled_number_value import NodeInputCompiledNumberValue
from .node_input_compiled_json_value import NodeInputCompiledJsonValue
from .node_input_compiled_chat_history_value import NodeInputCompiledChatHistoryValue
from .node_input_compiled_search_results_value import NodeInputCompiledSearchResultsValue
from .node_input_compiled_error_value import NodeInputCompiledErrorValue
from .node_input_compiled_array_value import NodeInputCompiledArrayValue
from .node_input_compiled_function_call_value import NodeInputCompiledFunctionCallValue

NodeInputVariableCompiledValue = typing.Union[
    NodeInputCompiledStringValue,
    NodeInputCompiledNumberValue,
    NodeInputCompiledJsonValue,
    NodeInputCompiledChatHistoryValue,
    NodeInputCompiledSearchResultsValue,
    NodeInputCompiledErrorValue,
    NodeInputCompiledArrayValue,
    NodeInputCompiledFunctionCallValue,
]