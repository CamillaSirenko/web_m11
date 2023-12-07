from pydantic import BaseModel
from datetime import datetime


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday:datetime
    additional_data: str = None

class ContactCreateUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday:datetime
    additional_data: str = None
