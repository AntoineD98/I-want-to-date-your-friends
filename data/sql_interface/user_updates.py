from sqlmodel import Session, create_engine, select, or_, and_
from typing import Any, Dict, Optional

from data.sql_model.user import User
from models.user_profile import UserProfile


#contains functions for updating user profile information
class UserUpdates:
    def __init__(self, db_url: str = "sqlite:///database.db"):
        self.engine = create_engine(db_url)
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(self.engine)

    def get_user(self, user_id: str) -> Optional[User]:
        with Session(self.engine) as session:
            return session.get(User, user_id)

    def add_user(self, user: User) -> bool:
        with Session(self.engine) as session:
            if session.get(User, user.user_id):
                return False  # User already exists
            session.add(user)
            session.commit()
            return True

    def update_user(self, user: User) -> bool:
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            return True
        
    def delete_user(self, user_id: str) -> bool:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False  # User does not exist
            session.delete(user)
            session.commit()
            return True

    def create_user_from_data(
        self,
        name: Optional[str] = None,
        node_only: bool = True,
        profile_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[User]:
        """Create and persist a user. Returns None if user_id already exists."""
        user = User(name=name, node_only=node_only)
        if profile_data:
            profile = UserProfile(**profile_data)
            user.set_profile(profile)
        if not self.add_user(user):
            return None
        return user

    def update_user_profile_from_data(
        self, user_id: str, profile_data: Dict[str, Any]
    ) -> Optional[User]:
        """Update a user's profile from a dict. Returns None if user not found."""
        user = self.get_user(user_id)
        if not user:
            return None
        profile = UserProfile(**profile_data)
        user.set_profile(profile)
        self.update_user(user)
        return user