import { exec } from "child_process";
import fs from "fs";
import { mkdir } from "fs/promises";
import { join } from "path";

import { python } from "@fern-api/python-ast";
import { AstNode } from "@fern-api/python-ast/core/AstNode";

import {
  GENERATED_DISPLAY_MODULE_NAME,
  GENERATED_DISPLAY_NODE_MODULE_PATH,
  GENERATED_NODES_MODULE_NAME,
  GENERATED_NODES_PATH,
} from "./constants";
import { createNodeContext, WorkflowContext } from "./context";
import { InputVariableContext } from "./context/input-variable-context";
import { InitFile, Inputs, Workflow } from "./generators";
import { BaseNode } from "./generators/nodes/bases";
import { GuardrailNode } from "./generators/nodes/guardrail-node";
import { SubworkflowNode } from "./generators/nodes/inline-subworkflow-node";
import { SearchNode } from "./generators/nodes/search-node";
import { TemplatingNode } from "./generators/nodes/templating-node";

import { codegen } from "./index";

import { ApiNodeContext } from "src/context/node-context/api-node";
import { BaseNodeContext } from "src/context/node-context/base";
import { CodeExecutionContext } from "src/context/node-context/code-execution-node";
import { ConditionalNodeContext } from "src/context/node-context/conditional-node";
import { ErrorNodeContext } from "src/context/node-context/error-node";
import { FinalOutputNodeContext } from "src/context/node-context/final-output-node";
import { GuardrailNodeContext } from "src/context/node-context/guardrail-node";
import { InlinePromptNodeContext } from "src/context/node-context/inline-prompt-node";
import { InlineSubworkflowNodeContext } from "src/context/node-context/inline-subworkflow-node";
import { MapNodeContext } from "src/context/node-context/map-node";
import { MergeNodeContext } from "src/context/node-context/merge-node";
import { NoteNodeContext } from "src/context/node-context/note-node";
import { TemplatingNodeContext } from "src/context/node-context/templating-node";
import { TextSearchNodeContext } from "src/context/node-context/text-search-node";
import { WorkflowOutputContext } from "src/context/workflow-output-context";
import { ApiNode } from "src/generators/nodes/api-node";
import { BaseNestedWorkflowNode } from "src/generators/nodes/bases/nested-workflow-base";
import { BaseSingleFileNode } from "src/generators/nodes/bases/single-file-base";
import { CodeExecutionNode } from "src/generators/nodes/code-execution-node";
import { ConditionalNode } from "src/generators/nodes/conditional-node";
import { ErrorNode } from "src/generators/nodes/error-node";
import { FinalOutputNode } from "src/generators/nodes/final-output-node";
import { InlinePromptNode } from "src/generators/nodes/inline-prompt-node";
import { MapNode } from "src/generators/nodes/map-node";
import { MergeNode } from "src/generators/nodes/merge-node";
import { NoteNode } from "src/generators/nodes/note-node";
import { WorkflowVersionExecConfigSerializer } from "src/serializers/vellum";
import {
  EntrypointNode,
  WorkflowDataNode,
  WorkflowNodeType as WorkflowNodeTypeEnum,
  WorkflowVersionExecConfig,
} from "src/types/vellum";
import { toSnakeCase } from "src/utils/casing";
import { assertUnreachable } from "src/utils/typing";

export class ProjectSerializationError extends Error {
  isProjectSerializationError = true;
}

export declare namespace WorkflowProjectGenerator {
  interface BaseArgs {
    workflowLabel?: string;
    moduleName?: string;
    workflowClassName?: string;
  }

  interface BaseProject extends BaseArgs {
    absolutePathToOutputDirectory: string;
    workflowsSdkModulePath?: readonly string[];
    workflowVersionExecConfigData: unknown;
  }

  interface NestedProject extends BaseArgs {
    workflowContext: WorkflowContext;
    workflowVersionExecConfig: WorkflowVersionExecConfig;
  }

  type Args = BaseProject | NestedProject;
}

export class WorkflowProjectGenerator {
  public readonly workflowVersionExecConfig: WorkflowVersionExecConfig;
  private readonly workflowContext: WorkflowContext;
  public readonly assets: {
    inputs: Inputs;
    workflow: Workflow;
    nodes: BaseNode<WorkflowDataNode, BaseNodeContext<WorkflowDataNode>>[];
  };

  constructor({
    workflowLabel = "Workflow",
    moduleName,
    workflowClassName,
    ...rest
  }: WorkflowProjectGenerator.Args) {
    if ("workflowContext" in rest) {
      this.workflowContext = rest.workflowContext;
      this.workflowVersionExecConfig = rest.workflowVersionExecConfig;
    } else {
      const workflowVersionExecConfigResult =
        WorkflowVersionExecConfigSerializer.parse(
          rest.workflowVersionExecConfigData,
          {
            allowUnrecognizedUnionMembers: true,
            allowUnrecognizedEnumValues: true,
            unrecognizedObjectKeys: "strip",
          }
        );
      if (!workflowVersionExecConfigResult.ok) {
        const { errors } = workflowVersionExecConfigResult;
        if (errors.length) {
          throw new ProjectSerializationError(
            `Invalid Workflow Version exec config. Found ${
              errors.length
            } errors, including:
${errors.slice(0, 3).map((err) => {
  return `- ${err.message} at ${err.path.join(".")}`;
})}`
          );
        } else {
          throw new ProjectSerializationError(
            "Invalid workflow version exec config, but no errors were returned."
          );
        }
      }
      this.workflowVersionExecConfig = workflowVersionExecConfigResult.value;
      this.workflowContext = new WorkflowContext({
        workflowsSdkModulePath: rest.workflowsSdkModulePath,
        absolutePathToOutputDirectory: rest.absolutePathToOutputDirectory,
        moduleName: moduleName || toSnakeCase(workflowLabel),
        workflowLabel,
        workflowClassName,
      });
    }

    this.assets = this.generateAssets();
  }

  public getModuleName(): string {
    return this.workflowContext.moduleName;
  }

  public async generateCode(): Promise<void> {
    const { inputs, workflow, nodes } = this.assets;

    const absolutePathToModuleDirectory = join(
      this.workflowContext.absolutePathToOutputDirectory,
      this.workflowContext.moduleName
    );

    await mkdir(absolutePathToModuleDirectory, {
      recursive: true,
    });

    await Promise.all([
      // __init__.py
      this.generateRootInitFile().persist(),
      // display/__init__.py
      this.generateDisplayRootInitFile().persist(),
      // display/workflow.py
      workflow.getWorkflowDisplayFile().persist(),
      // inputs.py
      inputs.persist(),
      // workflow.py
      workflow.getWorkflowFile().persist(),
      // nodes/*
      ...this.generateNodeFiles(nodes),
    ]);

    const setupCfgPath = this.resolvePythonConfigFilePath();

    await new Promise((resolve, reject) => {
      exec(
        `python -m isort --sp ${setupCfgPath} ${this.workflowContext.absolutePathToOutputDirectory}`,
        (error: Error | null) => {
          if (error) {
            reject(error);
          } else {
            resolve(undefined);
          }
        }
      );
    });
  }

  private generateRootInitFile(): InitFile {
    let statements: AstNode[];

    const parentNode = this.workflowContext.parentNode;
    if (parentNode) {
      statements = [parentNode.generateNodeClass()];
    } else {
      statements = [
        python.codeBlock(`\
# flake8: noqa: F401, F403

from .display import *\
`),
      ];
    }

    const rootInitFile = codegen.initFile({
      workflowContext: this.workflowContext,
      modulePath: this.workflowContext.parentNode
        ? [...this.workflowContext.parentNode.getNodeModulePath()]
        : [this.workflowContext.moduleName],
      statements,
    });

    return rootInitFile;
  }

  private generateDisplayRootInitFile(): InitFile {
    let statements: AstNode[];

    const parentNode = this.workflowContext.parentNode;
    if (parentNode) {
      statements = parentNode.generateNodeDisplayClasses();
    } else {
      statements = [
        python.codeBlock(`\
# flake8: noqa: F401, F403

from .nodes import *
from .workflow import *\
`),
      ];
    }

    const rootDisplayInitFile = codegen.initFile({
      workflowContext: this.workflowContext,
      modulePath: this.workflowContext.parentNode
        ? [...this.workflowContext.parentNode.getNodeDisplayModulePath()]
        : [this.workflowContext.moduleName, GENERATED_DISPLAY_MODULE_NAME],
      statements,
    });

    return rootDisplayInitFile;
  }

  private generateAssets(): {
    inputs: Inputs;
    workflow: Workflow;
    nodes: BaseNode<WorkflowDataNode, BaseNodeContext<WorkflowDataNode>>[];
  } {
    const moduleName = this.workflowContext.moduleName;

    this.workflowVersionExecConfig.inputVariables.forEach((inputVariable) => {
      const inputVariableContext = new InputVariableContext({
        inputVariableData: inputVariable,
        workflowContext: this.workflowContext,
      });
      this.workflowContext.addInputVariableContext(inputVariableContext);
    });

    let entrypointNode: EntrypointNode | undefined;
    const nodesToGenerate: WorkflowDataNode[] = [];
    this.workflowVersionExecConfig.workflowRawData.nodes.forEach((nodeData) => {
      if (nodeData.type === "TERMINAL") {
        this.workflowContext.addWorkflowOutputContext(
          new WorkflowOutputContext({
            terminalNodeData: nodeData,
          })
        );
      } else if (nodeData.type === "ENTRYPOINT") {
        if (entrypointNode) {
          throw new Error("Multiple entrypoint nodes found");
        }
        entrypointNode = nodeData;
        return;
      }

      nodesToGenerate.push(nodeData);

      const nodeContext = createNodeContext({
        workflowContext: this.workflowContext,
        nodeData,
      });
      this.workflowContext.addNodeContext(nodeContext);
    });
    if (!entrypointNode) {
      throw new Error("Entrypoint node not found");
    }
    this.workflowContext.addEntrypointNode(entrypointNode);

    const inputs = codegen.inputs({
      workflowContext: this.workflowContext,
    });

    const nodeIds = nodesToGenerate.map((nodeData) => nodeData.id);
    const nodes = this.generateNodes(nodeIds);

    const workflow = codegen.workflow({
      moduleName,
      workflowContext: this.workflowContext,
      inputs,
      nodes: nodesToGenerate,
      edges: this.workflowVersionExecConfig.workflowRawData.edges,
      displayData: this.workflowVersionExecConfig.workflowRawData.displayData,
    });

    return { inputs, workflow, nodes };
  }

  private generateNodes(
    nodeIds: string[]
  ): BaseNode<WorkflowDataNode, BaseNodeContext<WorkflowDataNode>>[] {
    const nodes: BaseNode<
      WorkflowDataNode,
      BaseNodeContext<WorkflowDataNode>
    >[] = [];

    nodeIds.forEach(async (nodeId) => {
      let node: BaseNode<WorkflowDataNode, BaseNodeContext<WorkflowDataNode>>;

      const nodeContext = this.workflowContext.getNodeContext(nodeId);
      const nodeData = nodeContext.nodeData;

      const nodeType = nodeData.type;
      switch (nodeType) {
        case WorkflowNodeTypeEnum.SEARCH: {
          node = new SearchNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as TextSearchNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.SUBWORKFLOW: {
          const variant = nodeData.data.variant;
          switch (variant) {
            case "INLINE":
              node = new SubworkflowNode({
                workflowContext: this.workflowContext,
                nodeContext: nodeContext as InlineSubworkflowNodeContext,
              });
              break;
            case "DEPLOYMENT":
              // TODO: https://app.shortcut.com/vellum/story/5269
              throw new Error(`DEPLOYMENT variant not yet supported`);
            default: {
              assertUnreachable(variant);
            }
          }
          break;
        }
        case WorkflowNodeTypeEnum.MAP: {
          const mapNodeVariant = nodeData.data.variant;
          switch (mapNodeVariant) {
            case "INLINE":
              node = new MapNode({
                workflowContext: this.workflowContext,
                nodeContext: nodeContext as MapNodeContext,
              });
              break;
            case "DEPLOYMENT":
              throw new Error(`DEPLOYMENT variant not yet supported`);
            default: {
              assertUnreachable(mapNodeVariant);
            }
          }
          break;
        }
        case WorkflowNodeTypeEnum.METRIC: {
          node = new GuardrailNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as GuardrailNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.CODE_EXECUTION: {
          node = new CodeExecutionNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as CodeExecutionContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.PROMPT: {
          const promptNodeVariant = nodeData.data.variant;

          switch (promptNodeVariant) {
            case "INLINE":
              node = new InlinePromptNode({
                workflowContext: this.workflowContext,
                nodeContext: nodeContext as InlinePromptNodeContext,
              });
              break;
            case "DEPLOYMENT":
              // TODO: https://app.shortcut.com/vellum/story/5261
              throw new Error(`DEPLOYMENT variant not yet supported`);
            case "LEGACY":
              throw new Error(`LEGACY variant not yet supported`);
            default: {
              assertUnreachable(promptNodeVariant);
            }
          }
          break;
        }
        case WorkflowNodeTypeEnum.TEMPLATING: {
          node = new TemplatingNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as TemplatingNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.CONDITIONAL: {
          node = new ConditionalNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as ConditionalNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.TERMINAL: {
          node = new FinalOutputNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as FinalOutputNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.MERGE: {
          node = new MergeNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as MergeNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.ERROR: {
          node = new ErrorNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as ErrorNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.NOTE: {
          node = new NoteNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as NoteNodeContext,
          });
          break;
        }
        case WorkflowNodeTypeEnum.API:
          node = new ApiNode({
            workflowContext: this.workflowContext,
            nodeContext: nodeContext as ApiNodeContext,
          });
          break;
        default: {
          throw new Error(`Unsupported node type: ${nodeType}`);
        }
      }

      nodes.push(node);
    });

    return nodes;
  }

  private generateNodeFiles(
    nodes: BaseNode<WorkflowDataNode, BaseNodeContext<WorkflowDataNode>>[]
  ): Promise<void>[] {
    const rootNodesInitFileStatements: AstNode[] = [];
    const rootDisplayNodesInitFileStatements: AstNode[] = [];
    if (nodes.length) {
      const nodeInitFileAllField = python.field({
        name: "__all__",
        initializer: python.TypeInstantiation.list([
          ...nodes.map((node) => {
            return python.TypeInstantiation.str(node.getNodeClassName());
          }),
        ]),
      });
      rootNodesInitFileStatements.push(nodeInitFileAllField);

      const nodeDisplayInitFileAllField = python.field({
        name: "__all__",
        initializer: python.TypeInstantiation.list([
          ...nodes.map((node) => {
            return python.TypeInstantiation.str(node.getNodeDisplayClassName());
          }),
        ]),
      });
      rootDisplayNodesInitFileStatements.push(nodeDisplayInitFileAllField);
    }

    const rootNodesInitFile = codegen.initFile({
      workflowContext: this.workflowContext,
      modulePath: this.workflowContext.parentNode
        ? [
            ...this.workflowContext.parentNode.getNodeModulePath(),
            GENERATED_NODES_MODULE_NAME,
          ]
        : [this.workflowContext.moduleName, ...GENERATED_NODES_PATH],
      statements: rootNodesInitFileStatements,
    });

    const rootDisplayNodesInitFile = codegen.initFile({
      workflowContext: this.workflowContext,
      modulePath: this.workflowContext.parentNode
        ? [
            ...this.workflowContext.parentNode.getNodeDisplayModulePath(),
            GENERATED_NODES_MODULE_NAME,
          ]
        : [
            this.workflowContext.moduleName,
            ...GENERATED_DISPLAY_NODE_MODULE_PATH,
          ],
      statements: rootDisplayNodesInitFileStatements,
    });

    nodes.forEach((node) => {
      rootNodesInitFile.addReference(
        python.reference({
          name: node.getNodeClassName(),
          modulePath: node.getNodeModulePath(),
        })
      );

      rootDisplayNodesInitFile.addReference(
        python.reference({
          name: node.getNodeDisplayClassName(),
          modulePath: node.getNodeDisplayModulePath(),
        })
      );
    });

    const nodePromises: Promise<void>[] = [];
    nodes.forEach((node) => {
      if (node instanceof BaseSingleFileNode) {
        nodePromises.push(node.getNodeFile().persist());
        nodePromises.push(node.getNodeDisplayFile().persist());
      } else if (node instanceof BaseNestedWorkflowNode) {
        const nestedProjects = node.getNestedProjects();
        nestedProjects.forEach((project) => {
          nodePromises.push(project.generateCode());
        });

        // If this nested node, then it means we've already defined it's implementation and display classes in
        // init files at a previous step.
        return;
      }
    });

    return [
      // nodes/__init__.py
      rootNodesInitFile.persist(),
      // nodes/* and display/nodes/*
      ...nodePromises,
      // display/nodes/__init__.py
      rootDisplayNodesInitFile.persist(),
    ];
  }

  private resolvePythonConfigFilePath(): string {
    if (
      process.env.ISORT_SETUP_CFG &&
      fs.existsSync(process.env.ISORT_SETUP_CFG)
    ) {
      return process.env.ISORT_SETUP_CFG;
    }

    const cwdPyProjectTomlPath = join(process.cwd(), "pyproject.toml");
    if (fs.existsSync(cwdPyProjectTomlPath)) {
      return cwdPyProjectTomlPath;
    }

    const parentDirPyProjectTomlPath = join(
      process.cwd(),
      "..",
      "pyproject.toml"
    );
    if (fs.existsSync(parentDirPyProjectTomlPath)) {
      return parentDirPyProjectTomlPath;
    }

    const rootDirPyProjectTomlPath = join(
      process.cwd(),
      "..",
      "..",
      "pyproject.toml"
    );
    if (fs.existsSync(rootDirPyProjectTomlPath)) {
      return rootDirPyProjectTomlPath;
    }

    const cwdSetupCfgPath = join(process.cwd(), "setup.cfg");
    if (fs.existsSync(cwdSetupCfgPath)) {
      return cwdSetupCfgPath;
    }

    const parentDirSetupCfgPath = join(process.cwd(), "..", "setup.cfg");
    if (fs.existsSync(parentDirSetupCfgPath)) {
      return parentDirSetupCfgPath;
    }

    const rootDirSetupCfgPath = join(process.cwd(), "..", "..", "setup.cfg");
    if (fs.existsSync(rootDirSetupCfgPath)) {
      return rootDirSetupCfgPath;
    }

    throw new Error("No isort Config file found");
  }
}
