import { python } from "@fern-api/python-ast";
import { ClassInstantiation } from "@fern-api/python-ast/ClassInstantiation";
import { MethodArgument } from "@fern-api/python-ast/MethodArgument";
import { AstNode } from "@fern-api/python-ast/core/AstNode";
import { Writer } from "@fern-api/python-ast/core/Writer";
import { isNil } from "lodash";

import { WorkflowContext } from "src/context/workflow-context";
import {
  FunctionDefinitionPromptTemplateBlock,
  PromptTemplateBlock,
} from "src/types/vellum";

export type PromptTemplateBlockExcludingFunctionDefinition = Exclude<
  PromptTemplateBlock,
  FunctionDefinitionPromptTemplateBlock
>;

export declare namespace BasePromptBlock {
  interface Args<T extends PromptTemplateBlockExcludingFunctionDefinition> {
    workflowContext: WorkflowContext;
    promptBlock: T;
    inputVariableNameById: Record<string, string>;
  }
}

export abstract class BasePromptBlock<
  T extends PromptTemplateBlockExcludingFunctionDefinition
> extends AstNode {
  protected workflowContext: WorkflowContext;
  private astNode: python.ClassInstantiation;
  protected inputVariableNameById: Record<string, string>;

  public constructor({
    workflowContext,
    promptBlock,
    inputVariableNameById,
  }: BasePromptBlock.Args<T>) {
    super();
    this.workflowContext = workflowContext;
    this.inputVariableNameById = inputVariableNameById;
    this.astNode = this.generateAstNode(promptBlock);
  }

  protected abstract generateAstNode(promptBlock: T): ClassInstantiation;

  protected constructCommonClassArguments(promptBlock: T): MethodArgument[] {
    const args: MethodArgument[] = [];

    if (promptBlock.state) {
      args.push(
        new MethodArgument({
          name: "state",
          value: python.TypeInstantiation.str(promptBlock.state),
        })
      );
    }

    const cacheConfig = this.generateCacheConfig(promptBlock);
    if (cacheConfig) {
      args.push(
        new MethodArgument({
          name: "cache_config",
          value: cacheConfig,
        })
      );
    }

    return args;
  }

  private generateCacheConfig(promptBlock: T): python.AstNode | undefined {
    if (isNil(promptBlock.cacheConfig)) {
      return undefined;
    }

    if (!promptBlock.cacheConfig.type) {
      return undefined;
    }

    const cacheConfigType = python.TypeInstantiation.str(
      promptBlock.cacheConfig.type
    );

    return python.instantiateClass({
      classReference: python.reference({
        name: "EphemeralPromptCacheConfig",
        modulePath:
          this.workflowContext.sdkModulePathNames.VELLUM_TYPES_MODULE_PATH,
      }),
      arguments_: [
        new MethodArgument({ name: "type", value: cacheConfigType }),
      ],
    });

    return python.TypeInstantiation.none();
  }

  public write(writer: Writer): void {
    this.astNode.write(writer);
  }
}
