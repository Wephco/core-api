from pydantic import BaseModel
from typing import Any

class ApiResponse(BaseModel):
    status: int
    data: Any
    detail: str

    # this class config is added so that the pydantic model can read the values 
    # from an orm model created using sqlalchemy and other object like structures
    class Config:
        orm_mode = True