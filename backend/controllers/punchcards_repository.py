from fastapi import APIRouter, Depends
from backend.business_logic.services.punchcard_services import LoyaltyService

router = APIRouter(prefix="/loyalty")

@router.post("/punch/{user_id}")
async def punch(user_id: str, service: LoyaltyService = Depends()):
    return await service.add_punch_to_user(user_id)
