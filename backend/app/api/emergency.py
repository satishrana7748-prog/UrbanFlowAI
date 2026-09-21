from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/emergency",
    tags=["Emergency Management"]
)


# =========================
# Emergency Request Model
# =========================

class EmergencyRequest(BaseModel):
    vehicle_type: str
    vehicle_id: str
    start_junction: str
    destination_junction: str


# =========================
# Emergency Request API
# =========================

@router.post("/request")
def emergency_request(request: EmergencyRequest):

    return {
        "status": "success",
        "message": "Emergency request received",
        "emergency_vehicle": {
            "vehicle_type": request.vehicle_type,
            "vehicle_id": request.vehicle_id
        },
        "route_request": {
            "start": request.start_junction,
            "destination": request.destination_junction
        }
    }
