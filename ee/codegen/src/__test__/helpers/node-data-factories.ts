import {
  ChatMessagePromptBlock,
  FunctionDefinitionPromptBlock,
  JinjaPromptBlock,
  RichTextPromptBlock,
  VellumVariableType,
} from "vellum-ai/api";
import { VariablePromptBlock } from "vellum-ai/api/types/VariablePromptBlock";

import {
  EntrypointNode,
  GuardrailNode,
  SearchNode,
  FinalOutputNode,
  WorkflowNodeType,
  PromptNode,
  TemplatingNode,
  ConditionalNode,
  ApiNode,
  MergeNode,
} from "src/types/vellum";

export function entrypointNodeDataFactory(): EntrypointNode {
  return {
    id: "entrypoint",
    type: WorkflowNodeType.ENTRYPOINT,
    inputs: [],
    data: { label: "Entrypoint", sourceHandleId: "<source_handle_id>" },
  };
}

export function terminalNodeDataFactory(): FinalOutputNode {
  return {
    id: "terminal-node-1",
    type: WorkflowNodeType.TERMINAL,
    inputs: [
      {
        id: "node-input-id",
        key: "query",
        value: {
          combinator: "OR",
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "input-variable-id",
              },
            },
          ],
        },
      },
    ],
    data: {
      label: "Final Output",
      name: "query",
      targetHandleId: "target-handle-id",
      outputId: "output-id",
      outputType: "STRING",
      nodeInputId: "node-input-id",
    },
  };
}

export function mergeNodeDataFactory(): MergeNode {
  return {
    id: "merge-node-1",
    type: WorkflowNodeType.MERGE,
    inputs: [],
    data: {
      label: "Merge Node",
      mergeStrategy: "AWAIT_ALL",
      targetHandles: [
        {
          id: "target-handle-id-1",
        },
        {
          id: "target-handle-id-2",
        },
      ],
      sourceHandleId: "source-handle-id",
    },
  };
}

export function searchNodeDataFactory({
  errorOutputId,
}: {
  errorOutputId?: string;
} = {}): SearchNode {
  const nodeData: SearchNode = {
    id: "search",
    type: WorkflowNodeType.SEARCH,
    data: {
      label: "Search Node",
      sourceHandleId: "e4dedb66-0638-4f0c-9941-6420bfe353b2",
      targetHandleId: "370d712d-3369-424e-bcf7-f4da1aef3928",
      errorOutputId,
      resultsOutputId: "77839b3c-fe1c-4dcb-9c61-2fac827f729b",
      textOutputId: "d56d7c49-7b45-4933-9779-2bd7f82c2141",
      queryNodeInputId: "f3a0d8b9-7772-4db6-8e28-f49f8c4d9e2a",
      documentIndexNodeInputId: "b49bc1ab-2ad5-4cf2-8966-5cc87949900d",
      weightsNodeInputId: "1daf3180-4b92-472a-8665-a7703c84a94e",
      limitNodeInputId: "161d264e-d04e-4c37-8e50-8bbb4c90c46e",
      separatorNodeInputId: "4eddefc0-90d5-422a-aec2-bc94c8f1d83c",
      resultMergingEnabledNodeInputId: "dc9f880b-81bc-4644-b025-8f7d5db23a48",
      externalIdFiltersNodeInputId: "61933e79-b0c2-4e3c-bf07-e2d93b9d9c54",
      metadataFiltersNodeInputId: "7c43b315-d1f2-4727-9540-6cc3fd4641f3",
    },
    inputs: [
      {
        id: "f3a0d8b9-7772-4db6-8e28-f49f8c4d9e2a",
        key: "query",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "a6ef8809-346e-469c-beed-2e5c4e9844c5",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "b49bc1ab-2ad5-4cf2-8966-5cc87949900d",
        key: "document_index_id",
        value: {
          combinator: "OR",
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "d5beca61-aacb-4b22-a70c-776a1e025aa4",
              },
            },
          ],
        },
      },
      {
        id: "1daf3180-4b92-472a-8665-a7703c84a94e",
        key: "weights",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "JSON",
                value: {
                  semantic_similarity: 0.8,
                  keywords: 0.2,
                },
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "161d264e-d04e-4c37-8e50-8bbb4c90c46e",
        key: "limit",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "NUMBER",
                value: 8,
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "4eddefc0-90d5-422a-aec2-bc94c8f1d83c",
        key: "separator",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "\n\n#####\n\n",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "dc9f880b-81bc-4644-b025-8f7d5db23a48",
        key: "result_merging_enabled",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "True",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "61933e79-b0c2-4e3c-bf07-e2d93b9d9c54",
        key: "external_id_filters",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "JSON",
                value: null,
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "7c43b315-d1f2-4727-9540-6cc3fd4641f3",
        key: "metadata_filters",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "JSON",
                value: null,
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
  };

  return nodeData;
}

export function guardrailNodeDataFactory({
  errorOutputId,
}: {
  errorOutputId?: string;
} = {}): GuardrailNode {
  const nodeData: GuardrailNode = {
    id: "metric",
    type: WorkflowNodeType.METRIC,
    data: {
      label: "Guardrail Node",
      sourceHandleId: "92aafe31-101b-47d3-86f2-e261c7747c16",
      targetHandleId: "1817fbab-db21-4219-8b34-0e150ce78887",
      errorOutputId,
      metricDefinitionId: "589df5bd-8c0d-4797-9a84-9598ecd043de",
      releaseTag: "LATEST",
    },
    inputs: [
      {
        id: "3f917af8-03a4-4ca4-8d40-fa662417fe9c",
        key: "expected",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "a6ef8809-346e-469c-beed-2e5c4e9844c5",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "bed55ada-923e-46ef-8340-1a5b0b563dc1",
        key: "actual",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "1472503c-1662-4da9-beb9-73026be90c68",
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
  };
  return nodeData;
}

const generateBlockGivenType = (
  blockType: string
):
  | JinjaPromptBlock
  | ChatMessagePromptBlock
  | FunctionDefinitionPromptBlock
  | VariablePromptBlock
  | RichTextPromptBlock => {
  if (blockType === "JINJA") {
    return {
      blockType: "JINJA",
      template: "Summarize what this means {{ INPUT_VARIABLE }}",
      state: "ENABLED",
    };
  } else if (blockType === "CHAT_MESSAGE") {
    return {
      blockType: "CHAT_MESSAGE",
      blocks: [
        {
          blockType: "RICH_TEXT",
          blocks: [
            {
              blockType: "PLAIN_TEXT",
              text: "Summarize the following text:\n\n",
              state: "ENABLED",
            },
            {
              blockType: "VARIABLE",
              state: "ENABLED",
              inputVariable: "text",
            },
          ],
          state: "ENABLED",
        },
      ],
      chatRole: "SYSTEM",
      chatMessageUnterminated: false,
      state: "ENABLED",
    };
  } else if (blockType === "FUNCTION_DEFINITION") {
    return {
      blockType: "FUNCTION_DEFINITION",
      functionName: "functionTest",
      functionDescription: "This is a test function",
      state: "ENABLED",
    };
  } else if (blockType === "VARIABLE") {
    return {
      blockType: "VARIABLE",
      state: "ENABLED",
      inputVariable: "text",
    };
  } else if (blockType === "RICH_TEXT") {
    return {
      blockType: "RICH_TEXT",
      blocks: [
        {
          blockType: "PLAIN_TEXT",
          text: "Hello World!",
          state: "ENABLED",
        },
      ],
      state: "ENABLED",
    };
  } else {
    throw new Error("Unrecognized block type");
  }
};

export function inlinePromptNodeDataInlineVariantFactory({
  blockType,
  errorOutputId,
}: {
  blockType: string;
  errorOutputId?: string;
}): PromptNode {
  const block = generateBlockGivenType(blockType);
  const nodeData: PromptNode = {
    id: "7e09927b-6d6f-4829-92c9-54e66bdcaf80",
    type: WorkflowNodeType.PROMPT,
    data: {
      variant: "INLINE",
      label: "Prompt Node",
      outputId: "2d4f1826-de75-499a-8f84-0a690c8136ad",
      arrayOutputId: "771c6fba-5b4a-4092-9d52-693242d7b92c",
      errorOutputId,
      sourceHandleId: "dd8397b1-5a41-4fa0-8c24-e5dffee4fb98",
      targetHandleId: "3feb7e71-ec63-4d58-82ba-c3df829a2948",
      execConfig: {
        parameters: {
          temperature: 0.0,
          maxTokens: 1000,
          topP: 1.0,
          topK: 0,
          frequencyPenalty: 0.0,
          presencePenalty: 0.0,
          logitBias: {},
          customParameters: {},
        },
        inputVariables: [
          {
            id: "7b8af68b-cf60-4fca-9c57-868042b5b616",
            key: "text",
            type: "STRING",
          },
        ],
        promptTemplateBlockData: {
          blocks: [block],
          version: 1,
        },
      },
      mlModelName: "gpt-4o-mini",
    },
    inputs: [
      {
        id: "7b8af68b-cf60-4fca-9c57-868042b5b616",
        key: "text",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "90c6afd3-06cc-430d-aed1-35937c062531",
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
  };
  return nodeData;
}

export function inlinePromptNodeDataLegacyVariantFactory({
  blockType,
  errorOutputId,
}: {
  blockType: string;
  errorOutputId?: string;
}): PromptNode {
  const block = generateBlockGivenType(blockType);
  const nodeData: PromptNode = {
    id: "7e09927b-6d6f-4829-92c9-54e66bdcaf80",
    type: WorkflowNodeType.PROMPT,
    data: {
      variant: "LEGACY",
      label: "Prompt Node",
      outputId: "2d4f1826-de75-499a-8f84-0a690c8136ad",
      arrayOutputId: "771c6fba-5b4a-4092-9d52-693242d7b92c",
      errorOutputId,
      sourceHandleId: "dd8397b1-5a41-4fa0-8c24-e5dffee4fb98",
      targetHandleId: "3feb7e71-ec63-4d58-82ba-c3df829a2948",
      sandboxRoutingConfig: {
        version: 1,
        promptVersionData: {
          execConfig: {
            parameters: {
              temperature: 0.0,
              maxTokens: 1000,
              topP: 1.0,
              topK: 0,
              frequencyPenalty: 0.0,
              presencePenalty: 0.0,
              logitBias: {},
              customParameters: {},
            },
            inputVariables: [
              {
                id: "7b8af68b-cf60-4fca-9c57-868042b5b616",
                key: "text",
                type: "STRING",
              },
            ],
            promptTemplateBlockData: {
              blocks: [block],
              version: 1,
            },
          },
          mlModelToWorkspaceId: "gpt-4o-mini",
        },
      },
    },
    inputs: [
      {
        id: "7b8af68b-cf60-4fca-9c57-868042b5b616",
        key: "text",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "90c6afd3-06cc-430d-aed1-35937c062531",
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
  };
  return nodeData;
}

export function inlineTemplatingNodeDataFactory({
  errorOutputId,
}: {
  errorOutputId?: string;
} = {}): TemplatingNode {
  const nodeData: TemplatingNode = {
    id: "7e09927b-6d6f-4829-92c9-54e66bdcaf80",
    type: WorkflowNodeType.TEMPLATING,
    data: {
      label: "Templating Node",
      outputId: "2d4f1826-de75-499a-8f84-0a690c8136ad",
      errorOutputId,
      sourceHandleId: "dd8397b1-5a41-4fa0-8c24-e5dffee4fb98",
      targetHandleId: "3feb7e71-ec63-4d58-82ba-c3df829a2948",
      templateNodeInputId: "7b8af68b-cf60-4fca-9c57-868042b5b616",
      outputType: VellumVariableType.String,
    },
    inputs: [
      {
        id: "7b8af68b-cf60-4fca-9c57-868042b5b616",
        key: "text",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "Hello, world!",
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
  };
  return nodeData;
}

export function conditionalNodeFactory(): ConditionalNode {
  const nodeData: ConditionalNode = {
    id: "30bec4c1-d6fa-437e-9498-f55a7af91931",
    type: WorkflowNodeType.CONDITIONAL,
    data: {
      label: "Conditional Node",
      targetHandleId: "2dbef7bb-7a6c-4d05-9906-51089b621874",
      conditions: [
        {
          id: "8d0d8b56-6c17-4684-9f16-45dd6ce23060",
          type: "IF",
          sourceHandleId: "63345ab5-1a4d-48a1-ad33-91bec41f92a5",
          data: {
            id: "fa50fb0c-8d62-40e3-bd88-080b52efd4b2",
            rules: [
              {
                id: "ad6bcb67-f21b-4af9-8d4b-ac8d3ba297cc",
                rules: [],
                fieldNodeInputId: "2cb6582e-c329-4952-8598-097830b766c7",
                operator: "=",
                valueNodeInputId: "cf63d0ad-5e52-4031-a29f-922e7004cdd8",
              },
            ],
            combinator: "AND",
          },
        },
        {
          id: "ea63ccd5-3fe3-4371-ba3c-6d3ec7ca2b60",
          type: "ELSE",
          sourceHandleId: "14a8b603-6039-4491-92d4-868a4dae4c15",
        },
      ],
      version: "2",
    },
    inputs: [
      {
        id: "2cb6582e-c329-4952-8598-097830b766c7",
        key: "ad6bcb67-f21b-4af9-8d4b-ac8d3ba297cc.field",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "d2287fee-98fb-421c-9464-e54d8f70f046",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "cf63d0ad-5e52-4031-a29f-922e7004cdd8",
        key: "ad6bcb67-f21b-4af9-8d4b-ac8d3ba297cc.value",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "testtest",
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
    displayData: {
      width: 480,
      height: 180,
      position: {
        x: 2247.2797390213086,
        y: 30.917121251477084,
      },
    },
  };
  return nodeData;
}

export function ApiNodeFactory({
  errorOutputId,
}: {
  errorOutputId?: string;
} = {}): ApiNode {
  const nodeData: ApiNode = {
    id: "2cd960a3-cb8a-43ed-9e3f-f003fc480951",
    type: "API",
    data: {
      label: "API Node",
      methodInputId: "9bf086d4-feed-47ff-9736-a5a6aa3a11cc",
      urlInputId: "480a4c12-22d6-4223-a38a-85db5eda118c",
      bodyInputId: "74865eb7-cdaf-4d40-a499-0a6505e72680",
      authorizationTypeInputId: "de330dac-05b1-4e78-bee7-7452203af3d5",
      bearerTokenValueInputId: "931502c1-23a5-4e2a-a75e-80736c42f3c9",
      apiKeyHeaderKeyInputId: "96c8343d-cc94-4df0-9001-eb2905a00be7",
      apiKeyHeaderValueInputId: "bfc2e790-66fd-42fd-acf7-3b2c785c1a0a",
      additionalHeaders: [
        {
          headerKeyInputId: "8ad006f3-d19e-4af1-931f-3e955152cd91",
          headerValueInputId: "36865dca-40b4-432c-bab4-1e11bb9f4083",
        },
        {
          headerKeyInputId: "3075be8c-248b-421d-9266-7779297be883",
          headerValueInputId: "00baaee1-b785-403d-b391-f68b3aea334f",
        },
        {
          headerKeyInputId: "13c2dd5e-cdd0-431b-aa91-46ad8da1cb51",
          headerValueInputId: "408c2b3d-7c30-4e01-a2e3-276753beadbc",
        },
      ],
      textOutputId: "81b270c0-4deb-4db3-aae5-138f79531b2b",
      jsonOutputId: "af576eaa-d39d-4c19-8992-1f01a65a709a",
      statusCodeOutputId: "69250713-617d-42a4-9326-456c70d0ef20",
      errorOutputId,
      targetHandleId: "06573a05-e6f0-48b9-bc6e-07e06d0bc1b1",
      sourceHandleId: "c38a71f6-3ffb-45fa-9eea-93c6984a9e3e",
    },
    inputs: [
      {
        id: "9bf086d4-feed-47ff-9736-a5a6aa3a11cc",
        key: "method",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "POST",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "480a4c12-22d6-4223-a38a-85db5eda118c",
        key: "url",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "fasdfadsf",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "74865eb7-cdaf-4d40-a499-0a6505e72680",
        key: "body",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "JSON",
                value: {},
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "de330dac-05b1-4e78-bee7-7452203af3d5",
        key: "authorization_type",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: undefined,
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "931502c1-23a5-4e2a-a75e-80736c42f3c9",
        key: "bearer_token_value",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "<my-bearer-token>",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "96c8343d-cc94-4df0-9001-eb2905a00be7",
        key: "api_key_header_key",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "bfc2e790-66fd-42fd-acf7-3b2c785c1a0a",
        key: "api_key_header_value",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "<my-bearer-token>",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "8ad006f3-d19e-4af1-931f-3e955152cd91",
        key: "additional_header_key_1",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "foo",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "36865dca-40b4-432c-bab4-1e11bb9f4083",
        key: "additional_header_value_1",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "5f64210f-ec43-48ce-ae40-40a9ba4c4c11",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "3075be8c-248b-421d-9266-7779297be883",
        key: "additional_header_key_2",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "bar",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "00baaee1-b785-403d-b391-f68b3aea334f",
        key: "additional_header_value_2",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "b81c5c88-9528-47d0-8106-14a75520ed47",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "13c2dd5e-cdd0-431b-aa91-46ad8da1cb51",
        key: "additional_header_key_3",
        value: {
          rules: [
            {
              type: "CONSTANT_VALUE",
              data: {
                type: "STRING",
                value: "baz",
              },
            },
          ],
          combinator: "OR",
        },
      },
      {
        id: "408c2b3d-7c30-4e01-a2e3-276753beadbc",
        key: "additional_header_value_3",
        value: {
          rules: [
            {
              type: "INPUT_VARIABLE",
              data: {
                inputVariableId: "b81c5c88-9528-47d0-8106-14a75520ed47",
              },
            },
          ],
          combinator: "OR",
        },
      },
    ],
    displayData: {
      width: 462,
      height: 288,
      position: {
        x: 2075.7067885117494,
        y: 234.65663468515768,
      },
    },
  };
  return nodeData;
}