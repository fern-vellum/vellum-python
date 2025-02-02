import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";

import { WorkflowContext } from "src/context";
import {
  IterableConfig,
  NodeInputValuePointerRule as NodeInputValuePointerRuleType,
} from "src/types/vellum";

export declare namespace BaseNodeInputValuePointerRule {
  export interface Args<T extends NodeInputValuePointerRuleType> {
    workflowContext: WorkflowContext;
    nodeInputValuePointerRule: T;
    iterableConfig?: IterableConfig;
  }
}

export abstract class BaseNodeInputValuePointerRule<
  T extends NodeInputValuePointerRuleType
> extends AstNode {
  public readonly workflowContext: WorkflowContext;
  public readonly nodeInputValuePointerRule: T;
  public readonly iterableConfig?: IterableConfig;
  private astNode: AstNode | undefined;

  constructor({
    workflowContext,
    nodeInputValuePointerRule,
    iterableConfig,
  }: BaseNodeInputValuePointerRule.Args<T>) {
    super();
    this.workflowContext = workflowContext;
    this.iterableConfig = iterableConfig;
    this.nodeInputValuePointerRule = nodeInputValuePointerRule;

    this.astNode = this.getAstNode();
    if (this.astNode) {
      this.inheritReferences(this.astNode);
    }
  }

  abstract getAstNode(): AstNode | undefined;

  public write(writer: Writer): void {
    if (this.astNode) {
      this.astNode.write(writer);
    }
  }
}
