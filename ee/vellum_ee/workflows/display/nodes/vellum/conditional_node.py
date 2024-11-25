from dataclasses import dataclass
from uuid import UUID
from typing import Any, ClassVar, Dict, Generic, List, Optional, TypeVar

from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.nodes.vellum.utils import create_node_input
from vellum_ee.workflows.display.types import WorkflowDisplayContext
from vellum_ee.workflows.display.utils.uuids import uuid4_from_hash
from vellum_ee.workflows.display.vellum import NodeInput
from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.expressions.and_ import AndExpression
from vellum.workflows.expressions.begins_with import BeginsWithExpression
from vellum.workflows.expressions.between import BetweenExpression
from vellum.workflows.expressions.contains import ContainsExpression
from vellum.workflows.expressions.does_not_begin_with import DoesNotBeginWithExpression
from vellum.workflows.expressions.does_not_contain import DoesNotContainExpression
from vellum.workflows.expressions.does_not_end_with import DoesNotEndWithExpression
from vellum.workflows.expressions.does_not_equal import DoesNotEqualExpression
from vellum.workflows.expressions.ends_with import EndsWithExpression
from vellum.workflows.expressions.equals import EqualsExpression
from vellum.workflows.expressions.greater_than import GreaterThanExpression
from vellum.workflows.expressions.greater_than_or_equal_to import GreaterThanOrEqualToExpression
from vellum.workflows.expressions.in_ import InExpression
from vellum.workflows.expressions.is_not_null import IsNotNullExpression
from vellum.workflows.expressions.is_null import IsNullExpression
from vellum.workflows.expressions.less_than import LessThanExpression
from vellum.workflows.expressions.less_than_or_equal_to import LessThanOrEqualToExpression
from vellum.workflows.expressions.not_between import NotBetweenExpression
from vellum.workflows.expressions.not_in import NotInExpression
from vellum.workflows.expressions.or_ import OrExpression
from vellum.workflows.nodes.displayable import ConditionalNode
from vellum.workflows.types.core import JsonObject

_ConditionalNodeType = TypeVar("_ConditionalNodeType", bound=ConditionalNode)


@dataclass
class RuleIdMap:
    id: UUID
    lhs: Optional["RuleIdMap"]
    rhs: Optional["RuleIdMap"]


class BaseConditionalNodeDisplay(BaseNodeVellumDisplay[_ConditionalNodeType], Generic[_ConditionalNodeType]):
    source_handle_ids: ClassVar[Dict[int, UUID]]
    rule_ids: ClassVar[List[RuleIdMap]]

    def serialize(self, display_context: WorkflowDisplayContext, **kwargs: Any) -> JsonObject:
        node = self._node
        node_id = self.node_id

        node_inputs: List[NodeInput] = []
        source_handle_ids = self._get_source_handle_ids() or {}

        def serialize_rule(
            descriptor: BaseDescriptor, path: List[int], rule_id_map: Optional[RuleIdMap]
        ) -> Dict[str, Any]:
            rule_id = (
                str(rule_id_map.id)
                if rule_id_map is not None
                else str(uuid4_from_hash(f"{node_id}|rule|{','.join(str(p) for p in path)}"))
            )
            field_node_input_id = None
            value_node_input_id = None

            # Recursive step: Keep recursing until we hit the other descriptors
            if isinstance(descriptor, (AndExpression, OrExpression)):
                combinator = "AND" if isinstance(descriptor, AndExpression) else "OR"

                lhs = serialize_rule(descriptor._lhs, path + [0], rule_id_map.lhs if rule_id_map else None)
                rhs = serialize_rule(descriptor._rhs, path + [1], rule_id_map.rhs if rule_id_map else None)
                rules = [lhs, rhs]

                return {
                    "id": rule_id,
                    "rules": rules,
                    "combinator": combinator,
                    "negated": False,
                    "field_node_input_id": None,
                    "operator": None,
                    "value_node_input_id": None,
                }

            # Base cases for other descriptors
            elif isinstance(descriptor, (IsNullExpression, IsNotNullExpression)):
                expression_node_input = create_node_input(
                    node_id, f"{rule_id}.field", descriptor._expression, display_context, None
                )
                node_inputs.append(expression_node_input)
                field_node_input_id = expression_node_input.id
                operator = self._convert_descriptor_to_operator(descriptor)

            elif isinstance(descriptor, (BetweenExpression, NotBetweenExpression)):
                field_node_input = create_node_input(
                    node_id, f"{rule_id}.field", descriptor._value, display_context, None
                )
                value_node_input = create_node_input(
                    node_id, f"{rule_id}.value", f"{descriptor._start},{descriptor._end}", display_context, None
                )
                node_inputs.extend([field_node_input, value_node_input])
                operator = self._convert_descriptor_to_operator(descriptor)
                field_node_input_id = field_node_input.id
                value_node_input_id = value_node_input.id

            else:
                lhs = descriptor._lhs  # type: ignore[attr-defined]
                rhs = descriptor._rhs  # type: ignore[attr-defined]

                lhs_node_input = create_node_input(node_id, f"{rule_id}.field", lhs, display_context, None)
                node_inputs.append(lhs_node_input)

                if descriptor._rhs is not None:  # type: ignore[attr-defined]
                    rhs_node_input = create_node_input(node_id, f"{rule_id}.value", rhs, display_context, None)
                    node_inputs.append(rhs_node_input)
                    value_node_input_id = rhs_node_input.id

                operator = self._convert_descriptor_to_operator(descriptor)
                field_node_input_id = lhs_node_input.id

            return {
                "id": rule_id,
                "rules": None,
                "combinator": None,
                "negated": False,
                "field_node_input_id": field_node_input_id,
                "operator": operator,
                "value_node_input_id": value_node_input_id,
            }

        conditions = []
        for idx, port in enumerate(node.Ports):
            if port._condition is None or port._condition_type is None:
                continue

            condition_id = str(uuid4_from_hash(f"{node_id}|conditions|{idx}"))
            source_handle_id = str(source_handle_ids.get(idx) or uuid4_from_hash(f"{node_id}|handles|{idx}"))

            rule_ids = self._get_rule_ids()
            condition_rule = serialize_rule(port._condition, [idx], rule_ids[idx] if len(rule_ids) > idx else None)
            rules = condition_rule["rules"] if condition_rule["rules"] else [condition_rule]

            conditions.append(
                {
                    "id": condition_id,
                    "type": port._condition_type.value,
                    "source_handle_id": source_handle_id,
                    "data": {
                        "id": str(uuid4_from_hash(f"{condition_id}|rule_group")),
                        "rules": rules,
                        "combinator": "AND",
                        "negated": False,
                        "field_node_input_id": None,
                        "operator": None,
                        "value_node_input_id": None,
                    },
                }
            )

        return {
            "id": str(node_id),
            "type": "CONDITIONAL",
            "inputs": [node_input.dict() for node_input in node_inputs],
            "data": {
                "label": self.label,
                "target_handle_id": str(self.get_target_handle_id()),
                "conditions": conditions,  # type: ignore
                "version": "2",
            },
            "display_data": self.get_display_data().dict(),
            "definition": self.get_definition().dict(),
        }

    def _convert_descriptor_to_operator(self, descriptor: BaseDescriptor) -> str:
        if isinstance(descriptor, EqualsExpression):
            return "="
        elif isinstance(descriptor, DoesNotEqualExpression):
            return "!="
        elif isinstance(descriptor, LessThanExpression):
            return "<"
        elif isinstance(descriptor, GreaterThanExpression):
            return ">"
        elif isinstance(descriptor, LessThanOrEqualToExpression):
            return "<="
        elif isinstance(descriptor, GreaterThanOrEqualToExpression):
            return ">="
        elif isinstance(descriptor, ContainsExpression):
            return "contains"
        elif isinstance(descriptor, BeginsWithExpression):
            return "beginsWith"
        elif isinstance(descriptor, EndsWithExpression):
            return "endsWith"
        elif isinstance(descriptor, DoesNotContainExpression):
            return "doesNotContain"
        elif isinstance(descriptor, DoesNotBeginWithExpression):
            return "doesNotBeginWith"
        elif isinstance(descriptor, DoesNotEndWithExpression):
            return "doesNotEndWith"
        elif isinstance(descriptor, IsNullExpression):
            return "null"
        elif isinstance(descriptor, IsNotNullExpression):
            return "notNull"
        elif isinstance(descriptor, InExpression):
            return "in"
        elif isinstance(descriptor, NotInExpression):
            return "notIn"
        elif isinstance(descriptor, BetweenExpression):
            return "between"
        elif isinstance(descriptor, NotBetweenExpression):
            return "notBetween"
        else:
            raise ValueError(f"Unsupported descriptor type: {descriptor}")

    def _get_source_handle_ids(self) -> Dict[int, UUID]:
        return self._get_explicit_node_display_attr("source_handle_ids", Dict[int, UUID]) or {}

    def _get_rule_ids(self) -> List[RuleIdMap]:
        return self._get_explicit_node_display_attr("rule_ids", List[RuleIdMap]) or []