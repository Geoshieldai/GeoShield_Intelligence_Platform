from backend.spatial.data_manager import GeoDataManager
from core.workflow_engine import WorkflowEngine


manager = GeoDataManager()

manager.load_layer(
    "counties",
    "data/boundaries/Kenya_county.shp"
)

manager.load_layer(
    "roads",
    "data/roads/ken_roads.shp"
)

workflow = WorkflowEngine(manager)

event = {
    "type": "Fire",
    "longitude": 36.8219,
    "latitude": -1.2921,
    "brightness": 370,
    "frp": 15,
    "confidence": "h"
}

result = workflow.process(event)

print(result)