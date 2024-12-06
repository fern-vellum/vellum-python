export type CodegenErrorCode =
  | "PROJECT_SERIALIZATION_ERROR"
  | "NODE_ATTRIBUTE_GENERATION_ERROR"
  | "NODE_NOT_FOUND_ERROR";

export abstract class BaseCodegenError extends Error {
  abstract code: CodegenErrorCode;
}

/**
 * An error that raises when deserializing the request to codegen
 * into a valid Workflow project.
 */
export class ProjectSerializationError extends BaseCodegenError {
  code = "PROJECT_SERIALIZATION_ERROR" as const;
}

/**
 * An error that raises when generating a node attribute fails.
 */
export class NodeAttributeGenerationError extends BaseCodegenError {
  code = "NODE_ATTRIBUTE_GENERATION_ERROR" as const;
}

/**
 * An error that raises when a node is not found.
 */
export class NodeNotFoundError extends BaseCodegenError {
  code = "NODE_NOT_FOUND_ERROR" as const;
}
