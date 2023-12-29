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
        for obj in reservation:
            obj.pop('_id', None)

        return reservation

    async def view_reservation_by_user(self, passenger_name: str, passenger_email: str):
        # search for reservation based on the user
        search_query = {"passenger_name": passenger_name, "passenger_email": passenger_email}
        reservation = await collection.find(search_query).to_list(length=None)
        for obj in reservation:
            obj.pop('_id', None)

        return reservation
