from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from databases import Database

DATABASE_URL = "sqlite:///./risks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
database = Database(DATABASE_URL)
metadata = MetaData()

risks = Table(
    "risks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("category", String, nullable=False),
    Column("status", String, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("risk_id", Integer, ForeignKey("risks.id"), nullable=False),
    Column("assigned_to", String, nullable=False),
    Column("status", String, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
)

def init_db() -> None:
    metadata.create_all(engine)