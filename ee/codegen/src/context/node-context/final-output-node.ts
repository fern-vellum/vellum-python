import { BaseNodeContext } from "src/context/node-context/base";
import { PortContext } from "src/context/port-context";
import { FinalOutputNode } from "src/types/vellum";

export class FinalOutputNodeContext extends BaseNodeContext<FinalOutputNode> {
  baseNodeClassName = "FinalOutputNode";
  baseNodeDisplayClassName = "BaseFinalOutputNodeDisplay";

  protected getNodeOutputNamesById(): Record<string, string> {
    return {
      [this.nodeData.data.outputId]: "value",
    };
  }

  createPortContexts(): PortContext[] {
    return [];
  }
}
