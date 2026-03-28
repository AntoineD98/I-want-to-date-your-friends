from typing import Any, Dict, Optional

from data.repository.user_updates import UserUpdatesRepository


user_updates = UserUpdatesRepository()


def create_user(
    name: Optional[str] = None,
    node_only: bool = True,
    profile_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    user = user_updates.create_user_from_data(
        name=name,
        node_only=node_only,
        profile_data=profile_data,
    )
    if not user:
        raise ValueError("User already exists with the given user_id.")
    return user.model_dump()


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    if not user_id:
        raise ValueError("user_id is required.")
    user = user_updates.get_user(user_id)
    if not user:
        return None
    return user.model_dump()


def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    if not user_id:
        raise ValueError("user_id is required.")

    user = user_updates.update_user_profile_from_data(
        user_id=user_id,
        profile_data=profile_data,
    )
    if not user:
        raise ValueError("User does not exist.")
    return user.model_dump()


def delete_user(user_id: str) -> bool:
    if not user_id:
        raise ValueError("user_id is required.")
    deleted = user_updates.delete_user(user_id)
    if not deleted:
        raise ValueError("User does not exist.")
    return True

