import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import { OUTPUTS_CLASS_NAME } from "src/constants";
import { GuardrailNodeContext } from "src/context/node-context/guardrail-node";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { GuardrailNode as GuardrailNodeType } from "src/types/vellum";

export class GuardrailNode extends BaseSingleFileNode<
  GuardrailNodeType,
  GuardrailNodeContext
> {
  baseNodeClassName = "GuardrailNode";
  baseNodeDisplayClassName = "BaseGuardrailNodeDisplay";

  getNodeClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    if (!this.nodeData.data.metricDefinitionId) {
      throw new Error("metric_definition_id is required");
    }

    statements.push(
      python.field({
        name: "metric_definition",
        initializer: python.TypeInstantiation.str(
          this.nodeData.data.metricDefinitionId
        ),
      })
    );

    statements.push(
      python.field({
        name: "metric_inputs",
        initializer: python.TypeInstantiation.dict(
          Array.from(this.nodeInputsByKey.entries()).map(([key, value]) => ({
            key: python.TypeInstantiation.str(key),
            value: value,
          }))
        ),
      })
    );

    if (!this.nodeData.data.releaseTag) {
      throw new Error("release_tag is required");
    }

    statements.push(
      python.field({
        name: "release_tag",
        initializer: python.TypeInstantiation.str(
          this.nodeData.data.releaseTag
        ),
      })
    );

    return statements;
  }

  getNodeDisplayClassBodyStatements(): AstNode[] {
    const statements: AstNode[] = [];

    statements.push(
      python.field({
        name: "label",
        initializer: python.TypeInstantiation.str(this.nodeData.data.label),
      })
    );

    statements.push(
      python.field({
        name: "node_id",
        initializer: python.TypeInstantiation.uuid(this.nodeData.id),
      })
    );

    statements.push(
      python.field({
        name: "target_handle_id",
        initializer: python.TypeInstantiation.uuid(
          this.nodeData.data.targetHandleId
        ),
      })
    );

    statements.push(
      python.field({
        name: "metric_input_ids_by_name",
        initializer: python.TypeInstantiation.dict(
          this.nodeData.inputs.map((input) => ({
            key: python.TypeInstantiation.str(input.key),
            value: python.TypeInstantiation.uuid(input.id),
          }))
        ),
      })
    );

    return statements;
  }

  protected getOutputDisplay(): python.Field | undefined {
    const record = this.nodeContext.getNodeOutputNamesById();
    Promise.resolve(record).then((record) => {
      const scoreId = Object.keys(record).find(
        (key) => record[key] === "score"
      );
      if (!scoreId) {
        throw new Error(
          "Score id is not found in the guardrail node output displays"
        );
      }
      return python.field({
        name: "output_display",
        initializer: python.TypeInstantiation.dict([
          {
            key: python.reference({
              name: this.nodeContext.nodeClassName,
              modulePath: this.nodeContext.nodeModulePath,
              attribute: [OUTPUTS_CLASS_NAME, "score"],
            }),
            value: python.instantiateClass({
              classReference: python.reference({
                name: "NodeOutputDisplay",
                modulePath:
                  this.workflowContext.sdkModulePathNames
                    .NODE_DISPLAY_TYPES_MODULE_PATH,
              }),
              arguments_: [
                python.methodArgument({
                  name: "id",
                  value: python.TypeInstantiation.uuid(scoreId),
                }),
                python.methodArgument({
                  name: "name",
                  value: python.TypeInstantiation.str("score"),
                }),
              ],
            }),
          },
        ]),
      });
    });
    return undefined;
  }

  protected getErrorOutputId(): string | undefined {
    return this.nodeData.data.errorOutputId;
  }
}
