from pydantic import BaseModel

# Schema for incoming data when creating or updating an error
class ErrorCreate(BaseModel):
    error_code: str
    description: str

# Schema for returning data to the user (includes the ID)
class ErrorResponse(ErrorCreate):
    id: int

    class Config:
        from_attributes = True