import datetime

from pydantic import BaseModel

from .movement import Movement, Rotation
from app.schemas import movement


class Update(BaseModel):
    time: datetime.time
    err: int
    type_: str


class MovementUpdate(Update):
    movement: Movement
    rotation: Rotation


class ManualUpdateRequest(BaseModel):
    movement: Movement
    rotation: Rotation


class Point(BaseModel):
    lon: float
    lat: float


class PathUpdate(Update):
    points: list[Point]


class PathUpdateRequest(BaseModel):
    points: list[Point]
