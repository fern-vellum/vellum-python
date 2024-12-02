import { MetricDefinitionHistoryItem } from "vellum-ai/api";

import { BaseNodeContext } from "./base";

import { PortContext } from "src/context/port-context";
import { GuardrailNode as GuardrailNodeType } from "src/types/vellum";

export declare namespace GuardrailNodeContext {
  interface Args extends BaseNodeContext.Args<GuardrailNodeType> {
    metricDefinitionsHistoryItem: MetricDefinitionHistoryItem;
  }
}

export class GuardrailNodeContext extends BaseNodeContext<GuardrailNodeType> {
  public metricDefinitionsHistoryItem: MetricDefinitionHistoryItem;

  constructor(args: GuardrailNodeContext.Args) {
    super(args);

    this.metricDefinitionsHistoryItem = args.metricDefinitionsHistoryItem;
  }

  getNodeOutputNamesById(): Record<string, string> {
    return this.metricDefinitionsHistoryItem.outputVariables.reduce(
      (acc, variable) => {
        acc[variable.id] = variable.key;
        return acc;
      },
      {} as Record<string, string>
    );
  }

  createPortContexts(): PortContext[] {
    return [
      new PortContext({
        workflowContext: this.workflowContext,
        nodeContext: this,
        portId: this.nodeData.data.sourceHandleId,
      }),
    ];
  }
}
