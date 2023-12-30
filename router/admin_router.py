from fastapi import APIRouter, Path, Query
from model.ticket_modification_model import TicketModificationModel
from service.admin_service import AdminService

admin_router = APIRouter()


@admin_router.get("/reservation/ticket/{flight_id}")
async def get_reservation_by_flight_id(flight_id: str):
    """
    Search all the reservations for a given flight id
    """
    return await AdminService().view_reservation_by_flight(flight_id)


@admin_router.get("/reservation/ticket/")
async def get_reservation_by_passenger(
        passenger_name: str = Query(..., description="passenger name"),
        passenger_email: str = Query(..., description="passenger email address")):
    """
    Search all the reservations for a given user details
    """
    return await AdminService().view_reservation_by_user(passenger_name, passenger_email)


@admin_router.put("/reservation/ticket/{reservation_id}")
async def update_reservation(reservation_id: str, ticket_model: TicketModificationModel):
    """
    Modify a reservation - user name and email address can only be modified
    """
    return await AdminService().update_reservation(reservation_id, ticket_model)
