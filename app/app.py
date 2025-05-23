import datetime
from asyncio import Queue, TimeoutError, wait_for
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

from app.schemas import Update, MovementUpdate, PathUpdate, PathUpdateRequest
from app.schemas.updates import ManualUpdateRequest
from app.utils import Errors, UpdateTypes

app = FastAPI()

# In-memory queues per drone
queues: Dict[int, Queue[Update]] = {}


def get_or_create_queue(drone_id: int) -> Queue:
    if drone_id not in queues:
        queues[drone_id] = Queue()
    return queues[drone_id]


@app.get("/get_update/{drone_id}", response_model=Update)
async def get_update(drone_id: int):
    if drone_id not in queues:
        return Update(
            err=Errors.DRONE_NOT_FOUND,
            time=datetime.datetime.now().time(),
            type_=UpdateTypes.VOID,
        )

    try:
        update = await wait_for(queues[drone_id].get(), timeout=5.0)
        return update
    except TimeoutError:
        return Update(
            err=Errors.TIMEOUT,
            time=datetime.datetime.now().time(),
            type_=UpdateTypes.VOID,
        )


@app.get("/new/{drone_id}", response_model=Update)
async def new_drone(drone_id: int):
    get_or_create_queue(drone_id)
    return Update(
        err=Errors.OK,
        time=datetime.datetime.now().time(),
        type_=UpdateTypes.VOID,
    )


@app.post("/send/path/{drone_id}")
async def send_path_update(drone_id: int, payload: PathUpdateRequest):
    queue = get_or_create_queue(drone_id)
    now = datetime.datetime.now().time()

    update = PathUpdate(
        err=Errors.OK,
        time=now,
        type_=UpdateTypes.AUTO_PILOT_PATH,
        points=payload.points,
    )
    await queue.put(update)
    return {"status": "queued", "type": update.type_}


@app.post("/send/manual/{drone_id}")
async def send_manual_update(drone_id: int, payload: ManualUpdateRequest):
    queue = get_or_create_queue(drone_id)
    now = datetime.datetime.now().time()

    update = MovementUpdate(
        err=Errors.OK,
        time=now,
        type_=UpdateTypes.MANUAL,
        movement=payload.movement,
        rotation=payload.rotation,
    )
    await queue.put(update)
    return {"status": "queued", "type": update.type_}
