from bson import ObjectId
from fastapi import Query, HTTPException, Header
from model.ticket_modification_model import TicketModificationModel
from utils.db_utils import load_db

db = load_db()
collection = db["tickets"]


class AdminService:

    async def view_reservation_by_flight(self, flight_id: str):
        # Search for reservation based on the flight id
        reservation = await collection.find({"flight_id": flight_id}).to_list(length=None)
        if len(reservation) == 0:
            raise HTTPException(status_code=404, detail="Reservation not found")
        else:
            for obj in reservation:
                obj.pop('_id', None)

            return reservation

    async def view_reservation_by_user(self, passenger_name: str, passenger_email: str):
        # search for reservation based on the user
        search_query = {"passenger_name": passenger_name, "passenger_email": passenger_email}
        reservation = await collection.find(search_query).to_list(length=None)
        if len(reservation) == 0:
            raise HTTPException(status_code=404, detail="Reservation not found")
        else:
            for obj in reservation:
                obj.pop('_id', None)

            return reservation

    async def update_reservation(self,
                                 reservation_id: str, ticket_model: TicketModificationModel):
        # Update reservation details
        existing_reservation = await collection.find_one({"_id": ObjectId(reservation_id)})
        if existing_reservation is None:
            raise HTTPException(status_code=404, detail="Reservation not found")
        else:
            updated_reservation = await collection.find_one_and_update({"_id": ObjectId(reservation_id)},
                                                                       {"$set": ticket_model.dict()})
            updated_reservation.pop('_id', None)
            return {"message": "Reservation updated successfully", "updated_reservation": updated_reservation}
