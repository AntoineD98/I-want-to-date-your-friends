from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional


class ActionType(str, Enum):
    VIEWED = "viewed"
    LIKED = "liked"
    PASSED = "passed"

class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    viewer_id: str = Field(index=True)   
    target_id: str = Field(index=True)   
    action: ActionType = Field(default=ActionType.VIEWED)
    timestamp: datetime = Field(default_factory=datetime.now)