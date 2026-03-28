from fastapi import Depends
from sqlmodel import Session
from data.db.session import get_session
from .connection_repository import ConnectionRepository
from .user_interactions import UserInteractionsRepository
from .user_updates import UserUpdatesRepository

# ConnectionRepository dependency
def get_connection_repository(session: Session = Depends(get_session)):
    return ConnectionRepository(session)

# UserInteractionsRepository dependency
def get_user_interactions_repository(session: Session = Depends(get_session)):
    return UserInteractionsRepository(session)

# UserRepository dependency
def get_user_updates_repository(session: Session = Depends(get_session)):
    return UserUpdatesRepository(session)

