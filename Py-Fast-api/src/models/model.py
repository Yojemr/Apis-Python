from typing import Optional
from pydantic import BaseModel, EmailStr

class TraineeModel(BaseModel):
    document: str
    firstname: str
    lastname: str
    email: EmailStr
    age: int
    program :str
    record_number: int

class TraineeUpdateModel(BaseModel):
    fistname: Optional[str] = none
    lastname: Optional[str] = none
    email: Optional[EmailStr] = none
    age: Optional[int] = none
    program: Optional[str] = none
    record_number: Optional[int] = none