from pydantic import BaseModel


class TicketModificationModel(BaseModel):
    passenger_email: str
    passenger_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "passenger_email": "john.doe@example.com",
                "passenger_name": "John Doe",
            }
        }