from pydantic import BaseModel, Field


class AdminRegister(BaseModel):
    name: str
    email: str
    password: str
    confirmPassword:  str

class AdminRead(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True

class AdminUpdate(BaseModel):
    name: str | None = Field(default=None)