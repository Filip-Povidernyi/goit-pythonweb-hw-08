from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ContactModel(BaseModel):

    name: str = Field(max_length=30, min_length=3)
    last_name: str = Field(max_length=50, min_length=1)
    email: str = Field(max_length=100, min_length=5)
    phone: str = Field(max_length=15, min_length=7)
    birthday: datetime


class ContactResponse(ContactModel):
    id: int
    created_at: datetime | None
    updated_at: Optional[datetime] | None
    model_config = ConfigDict(from_attributes=True)
