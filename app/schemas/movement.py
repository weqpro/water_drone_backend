from pydantic import BaseModel


class Movement(BaseModel):
    direction: bool
    duration: int


class Rotation(BaseModel):
    angle: float
