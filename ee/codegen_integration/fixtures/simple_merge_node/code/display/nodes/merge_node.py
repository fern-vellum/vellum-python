from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseMergeNodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.merge_node import MergeNode


class MergeNodeDisplay(BaseMergeNodeDisplay[MergeNode]):
    target_handle_ids = [UUID("cf6974a6-1676-43ed-99a0-66bd3eac235f"), UUID("dee0633e-0221-40c7-b179-aae1cf67de87")]
    node_input_ids_by_name = {}
    port_displays = {MergeNode.Ports.default: PortDisplayOverrides(id=UUID("e0e666c4-a90b-4a95-928e-144bab251356"))}
    display_data = NodeDisplayData(
        position=NodeDisplayPosition(x=2374.2549861495845, y=205.20096952908594), width=476, height=180
    )
