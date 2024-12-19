import { python } from "@fern-api/python-ast";
import { MethodArgument } from "@fern-api/python-ast/MethodArgument";
import { OperatorType } from "@fern-api/python-ast/OperatorType";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";
import { isNil } from "lodash";

import { PortContext } from "src/context/port-context";
import { Expression } from "src/generators/expression";
import { NodeInput } from "src/generators/node-inputs";
import {
  ConditionalNodeConditionData,
  ConditionalRuleData,
} from "src/types/vellum";

export declare namespace ConditionalNodePort {
  export interface Args {
    portContext: PortContext;
    inputFieldKeysByRuleId: Map<string, string>;
    valueInputKeysByRuleId: Map<string, string>;
    conditionData: ConditionalNodeConditionData;
    nodeInputsByKey: Map<string, NodeInput>;
  }
}

export class ConditionalNodePort extends AstNode {
  private portContext: PortContext;
  private conditionalNodeData: ConditionalNodeConditionData;
  private inputFieldKeysByRuleId: Map<string, string>;
  private valueInputKeysByRuleId: Map<string, string>;
  private nodeInputsByKey: Map<string, NodeInput>;
  private astNode: AstNode;

  public constructor(args: ConditionalNodePort.Args) {
    super();

    this.portContext = args.portContext;
    this.inputFieldKeysByRuleId = args.inputFieldKeysByRuleId;
    this.valueInputKeysByRuleId = args.valueInputKeysByRuleId;
    this.conditionalNodeData = args.conditionData;
    this.nodeInputsByKey = args.nodeInputsByKey;
    this.astNode = this.constructPort();
    this.inheritReferences(this.astNode);
  }

  private constructPort(): AstNode {
    return python.invokeMethod({
      methodReference: python.reference({
        name: "Port",
        modulePath:
          this.portContext.workflowContext.sdkModulePathNames.PORTS_MODULE_PATH,
        attribute: [
          this.convertConditionTypeToPortAttribute(
            this.conditionalNodeData.type
          ),
        ],
      }),
      arguments_: (() => {
        const arg = this.generatePortCondition();
        return arg ? [arg] : [];
      })(),
    });
  }

  private generatePortCondition() {
    const conditionData = this.conditionalNodeData.data;
    if (conditionData) {
      return new MethodArgument({
        value: this.buildCondition(conditionData),
      });
    } else {
      return undefined;
    }
  }

  private buildCondition(
    conditionData: ConditionalRuleData | undefined
  ): AstNode {
    if (!conditionData) {
      return python.TypeInstantiation.none();
    }

    if (conditionData && conditionData.fieldNodeInputId) {
      return this.buildDescriptor(conditionData);
    }

    const otherConditions = (conditionData.rules || []).map((rule) => {
      return this.buildCondition(rule);
    });

    const combine =
      conditionData.combinator === "AND"
        ? (lhs: AstNode, rhs: AstNode): AstNode => {
            return python.operator({
              operator: OperatorType.And,
              lhs: lhs,
              rhs: rhs,
            });
          }
        : (lhs: AstNode, rhs: AstNode): AstNode => {
            return python.operator({
              operator: OperatorType.Or,
              lhs: lhs,
              rhs: rhs,
            });
          };

    const combinedConditions = otherConditions.reduce((prev, curr) => {
      return combine(prev, curr);
    });
    return combinedConditions;
  }

  private convertConditionTypeToPortAttribute(conditionType: string): string {
    switch (conditionType) {
      case "IF":
        return "on_if";
      case "ELIF":
        return "on_elif";
      default:
        return "on_else";
    }
  }

  private buildDescriptor(conditionData: ConditionalRuleData): AstNode {
    const ruleId = conditionData.id;

    const lhsKey = this.inputFieldKeysByRuleId.get(ruleId);
    let rhsKey;
    if (isNil(lhsKey)) {
      throw new Error(`Could not find input field key given rule id ${ruleId}`);
    }
    if (conditionData.valueNodeInputId) {
      rhsKey = this.valueInputKeysByRuleId.get(ruleId);
    }
    const lhs = this.nodeInputsByKey.get(lhsKey);
    const rhs = !isNil(rhsKey) ? this.nodeInputsByKey.get(rhsKey) : undefined;
    const expression = conditionData.operator
      ? this.convertOperatorToMethod(conditionData.operator)
      : undefined;
    if (isNil(lhs) || isNil(expression)) {
      throw new Error("Port conditions require a lhs and an expression");
    }
    return new Expression({
      lhs: lhs,
      expression: expression,
      rhs: rhs,
    });
  }

  private convertOperatorToMethod(operator: string): string {
    const operatorMappings: { [key: string]: string } = {
      "=": "equals",
      "!=": "does_not_equal",
      "<": "less_than",
      ">": "greater_than",
      "<=": "less_than_or_equal_to",
      ">=": "greater_than_or_equal_to",
      contains: "contains",
      beginsWith: "begins_with",
      endsWith: "ends_with",
      doesNotContain: "does_not_contain",
      doesNotBeginWith: "does_not_begin_with",
      doesNotEndWith: "does_not_end_with",
      null: "is_none",
      notNull: "is_not_none",
      in: "in",
      notIn: "not_in",
      between: "between",
      notBetween: "not_between",
    };
    const value = operatorMappings[operator];
    if (!value) {
      throw new Error(`This operator: ${operator} is not supported`);
    }
    return value;
  }

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}
