import uuid

from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON


from models.user_profile import UserProfile
from models.endorsement import Endorsement


class User(SQLModel, table=True):
    user_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        primary_key=True,
        nullable=False
        )
    name : Optional[str] = Field(default=None, index=True) #User's preferred name for display purposes
    node_only: bool = Field(default=True, index=True) #True if this user is not a displaying profile, just an endorsement node
    profile_data: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    
    def set_profile(self, profile: UserProfile):
        self.profile_data = profile.model_dump()

    def get_profile(self) -> Optional[UserProfile]:
        if self.profile_data:
            return UserProfile(**self.profile_data)
        return None

    def change_node_only(self, node_only: bool):
        self.node_only = node_only
    