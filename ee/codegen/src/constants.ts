/* Module paths */
export const VELLUM_CLIENT_MODULE_PATH = ["vellum"] as const;

/* Class names */
export const OUTPUTS_CLASS_NAME = "Outputs";
export const PORTS_CLASS_NAME = "Ports";
export const DEFAULT_PORT_NAME = "default";

/* File names */
export const INIT_FILE_NAME = "__init__.py";

export const GENERATED_WORKFLOW_MODULE_NAME = "workflow";

export const GENERATED_INPUTS_MODULE_NAME = "inputs";

export const GENERATED_NODES_MODULE_NAME = "nodes";

export const GENERATED_DISPLAY_MODULE_NAME = "display";
export const GENERATED_NODES_PATH = [GENERATED_NODES_MODULE_NAME] as const;

export const GENERATED_DISPLAY_NODE_MODULE_PATH = [
  GENERATED_DISPLAY_MODULE_NAME,
  GENERATED_NODES_MODULE_NAME,
] as const;

export const GENERATED_NESTED_NODE_MODULE_NAME = "node";
