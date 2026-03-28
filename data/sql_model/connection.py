from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from datetime import datetime

#endorsement becomes connection when approved by recipient.
class ConnectionBase(SQLModel):
    # The Relationship "Edges"
    endorser_id: str = Field(index=True)
    recipient_id: str = Field(index=True)
    
    endorsement_data: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.now)

class PendingConnection(ConnectionBase, table=True):
    # Database Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

class Connection(ConnectionBase, table=True):
    # Database Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
