import {
  ErrorLogFile,
  InitFile,
  Inputs,
  NodeInput,
  VellumValue,
  VellumVariable,
  Workflow,
} from "./generators";
import { BasePersistedFile } from "./generators/base-persisted-file";
import { SandboxFile } from "./generators/sandbox-file";

export function vellumVariable(args: VellumVariable.Args): VellumVariable {
  return new VellumVariable(args);
}

export function vellumValue(args: VellumValue.Args): VellumValue {
  return new VellumValue(args);
}

export function nodeInput(args: NodeInput.Args): NodeInput {
  return new NodeInput(args);
}

export function inputs(args: Inputs.Args): Inputs {
  return new Inputs(args);
}

export function workflow(args: Workflow.Args): Workflow {
  return new Workflow(args);
}

export function initFile(args: InitFile.Args): InitFile {
  return new InitFile(args);
}

export function errorLogFile(args: BasePersistedFile.Args): ErrorLogFile {
  return new ErrorLogFile(args);
}

export function sandboxFile(args: SandboxFile.Args): SandboxFile {
  return new SandboxFile(args);
}
