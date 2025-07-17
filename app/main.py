import asyncio
import time
from typing import List
from fastapi import FastAPI, HTTPException, BackgroundTasks

from app.database import database, engine, init_db, risks, tasks
from app import schemas

#init_db()  #comment this 

app = FastAPI(title="Risk Assessment + Tasks Workflow", version="0.4.0")

# @app.on_event("startup")
# async def startup() -> None:
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown() -> None:
#     await database.disconnect()

async def _workflow_create_tasks(risk_id: int) -> None:
    await asyncio.sleep(10)
    now = time.time()
    for person in ("safety officer", "team leader"):
        await database.execute(
            tasks.insert().values(
                risk_id=risk_id,
                assigned_to=person,
                status="pending",
                created_at=now,
                updated_at=now,
            )
        )
    await database.execute(
        risks.update()
        .where(risks.c.id == risk_id)
        .values(status="completed", updated_at=time.time())
    )

@app.post("/risks", response_model=schemas.RiskOut, status_code=201)
async def create_risk(risk_in: schemas.RiskIn, bg: BackgroundTasks):
    now = time.time()
    risk_id = await database.execute(
        risks.insert().values(
            title=risk_in.title,
            description=risk_in.description,
            category=risk_in.category,
            status="in process",
            created_at=now,
            updated_at=now,
        )
    )
    bg.add_task(_workflow_create_tasks, risk_id)
    risk = await database.fetch_one(risks.select().where(risks.c.id == risk_id))
    return schemas.RiskOut(**risk)

@app.get("/risks", response_model=List[schemas.RiskOut])
async def list_risks():
    rows = await database.fetch_all(risks.select())
    return [schemas.RiskOut(**row) for row in rows]

@app.get("/risks/{risk_id}", response_model=schemas.RiskOut)
async def get_risk(risk_id: int):
    row = await database.fetch_one(risks.select().where(risks.c.id == risk_id))
    if not row:
        raise HTTPException(status_code=404, detail="Risk not found")
    return schemas.RiskOut(**row)

@app.get("/risks/{risk_id}/tasks", response_model=List[schemas.TaskOut])
async def get_risk_tasks(risk_id: int):
    rows = await database.fetch_all(tasks.select().where(tasks.c.risk_id == risk_id))
    return [schemas.TaskOut(**row) for row in rows]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Hazard Assessment API!"}

