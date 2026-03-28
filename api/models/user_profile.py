from pydantic import BaseModel, Field
from typing import Optional
from models.interests import Interests
from models.attributes import Background, Lifestyle, Personality
from models.endorsement import Endorsement

class UserProfile(BaseModel):
    interests: Optional[Interests] = None
    background: Optional[Background] = None
    lifestyle: Optional[Lifestyle] = None
    personality: Optional[Personality] = None
    looking_for: Optional[str] = Field(None, description="What the user is looking for in a match")
    excited_about: Optional[str] = Field(None, description="What the user is currently excited about")
    recent_activities: Optional[list[str]] = Field(default_factory=list, description="List of user's recent activities")
    most_important: Optional[str] = Field(None, description="What the user thinks is most important about themselves")
    deal_breakers: Optional[str] = Field(None, description="What the user considers deal breakers in a relationship")