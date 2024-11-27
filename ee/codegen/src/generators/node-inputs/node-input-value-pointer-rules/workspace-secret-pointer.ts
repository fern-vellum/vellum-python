import { python } from "@fern-api/python-ast";
import { isNil } from "lodash";

import { BaseNodeInputValuePointerRule } from "./base";

import { WorkspaceSecretPointer as WorkspaceSecretPointerType } from "src/types/vellum";

export class WorkspaceSecretPointerRule extends BaseNodeInputValuePointerRule<WorkspaceSecretPointerType> {
  getAstNode(): python.AstNode {
    const workspaceSecretPointerData = this.nodeInputValuePointerRule.data;

    const workspaceSecretName = workspaceSecretPointerData.workspaceSecretId;

    return python.instantiateClass({
      classReference: python.reference({
        name: "VellumSecretReference",
        modulePath: [
          ...this.workflowContext.sdkModulePathNames.WORKFLOWS_MODULE_PATH,
          "references",
        ],
      }),
      arguments_: [
        python.methodArgument({
          value: isNil(workspaceSecretName)
            ? python.TypeInstantiation.none()
            : python.TypeInstantiation.str(workspaceSecretName),
        }),
      ],
    });
  }
}
