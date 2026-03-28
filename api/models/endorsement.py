from pydantic import BaseModel, Field
from typing import Optional

class Endorsement(BaseModel):
    endorser_id: str
    endorser_name: Optional[str] = Field(None, description="Display name of the endorser")
    connection: Optional[str] = Field(None, description="How the endorser knows the user (e.g. friend, coworker, family)")
    favorite_qualities: Optional[str] = Field(None, description="What the endorser thinks are the user's best qualities")
    shared_experiences: Optional[str] = Field(None, description="Memories or experiences the endorser shared with the user that highlight their connection")
    