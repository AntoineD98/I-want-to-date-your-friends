from typing import Optional

from data.sql_model.user import User


#contains functions for updating user profile information
class UserUpdatesRepository:
    def __init__(self, session):
        self.session=session

    def get_user(self, user_id: str) -> Optional[User]:
        return self.session.get(User, user_id)

    def add_user(self, user: User) -> bool:
        if self.session.get(User, user.user_id):
            return False  # User already exists
        self.session.add(user)
        self.session.commit()
        return True

    def update_user(self, user: User) -> bool:
        self.session.add(user)
        self.session.commit()
        return True
        
    def delete_user(self, user_id: str) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False  # User does not exist
        self.session.delete(user)
        self.session.commit()
        return True
