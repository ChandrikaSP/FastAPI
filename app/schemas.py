from pydantic import BaseModel, Field

class RiskIn(BaseModel):
    title: str = Field(..., example="Late delivery")
    description: str = Field(..., example="Supplier X has a history …")
    category: str = Field(..., example="Supply‑Chain")

class RiskOut(RiskIn):
    id: int
    status: str
    created_at: float
    updated_at: float

class TaskOut(BaseModel):
    id: int
    risk_id: int
    assigned_to: str
    status: str
    created_at: float
    updated_at: float