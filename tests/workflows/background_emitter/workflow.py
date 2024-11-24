import time

from vellum.workflows import BaseWorkflow
from vellum.workflows.emitters.base import BaseWorkflowEmitter
from vellum.workflows.events.workflow import WorkflowEvent
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.state.base import BaseState


class ExpensiveEmitter(BaseWorkflowEmitter):
    def emit_event(self, event: WorkflowEvent) -> None:
        time.sleep(0.02)

    def snapshot_state(self, state: BaseState) -> None:
        time.sleep(0.02)


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        start_time: float

    def run(self) -> Outputs:
        return self.Outputs(start_time=time.time())


class EndNode(BaseNode):
    start_time = StartNode.Outputs.start_time

    class Outputs(BaseNode.Outputs):
        duration: float

    def run(self) -> Outputs:
        return self.Outputs(duration=time.time() - self.start_time)


class BackgroundEmitterWorkflow(BaseWorkflow):
    """
    A Workflow with an expensive data emitter. It records the duration
    of StartNode to EndNode to ensure that it's not blocked by the emitter.
    """

    graph = StartNode >> EndNode

    emitters = [ExpensiveEmitter()]

    class Outputs(BaseWorkflow.Outputs):
        final_value = EndNode.Outputs.duration
