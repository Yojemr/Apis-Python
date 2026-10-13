from typing import Optional

from pydantic import BaseModel, EmailStr


class TraineeModel(BaseModel):
    document: str
    firstname: str
    lastname: str
    email: EmailStr
    age: int
    program: str
    record_number: int


class TraineeUpdateModel(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    program: Optional[str] = None
    record_number: Optional[int] = None
