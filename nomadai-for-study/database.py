from sqlmodel import SQLModel, Field, create_engine
from datetime import datetime
from typing import Optional

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    sender: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

SQLITE_DATABASE_URL = "sqlite:///./chat_history.db"
engine = create_engine(SQLITE_DATABASE_URL)

def create_tables():
    SQLModel.metadata.create_all(engine)