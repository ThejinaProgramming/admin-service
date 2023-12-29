from fastapi import APIRouter, Path, Query
from model.ticket_modification_model import TicketModificationModel
from service.admin_service import AdminService

admin_router = APIRouter()


@admin_router.get("/reservation/ticket/{flight_id}")
async def get_reservation_by_flight_id(flight_id: str):
    return await AdminService().view_reservation_by_flight(flight_id)