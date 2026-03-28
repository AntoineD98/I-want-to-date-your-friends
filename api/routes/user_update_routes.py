from typing import Any, Dict, Optional, TypedDict

from fastapi import APIRouter, Body, HTTPException

from api.services.user_update_service import (
    create_user,
    delete_user,
    get_user,
    update_user_profile,
)


router = APIRouter(prefix="/users", tags=["users"])


class CreateUserPayload(TypedDict, total=False):
    name: Optional[str]
    node_only: bool
    profile: Optional[Dict[str, Any]]


class UpdateUserProfilePayload(TypedDict):
    profile: Dict[str, Any]


@router.post("", status_code=201)
def create_user_route(
    payload: CreateUserPayload = Body(...),
):
    try:
        return create_user(
            name=payload.get("name"),
            node_only=payload.get("node_only", True),
            profile_data=payload.get("profile"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{user_id}")
def get_user_route(user_id: str):
    try:
        data = get_user(user_id)
        if not data:
            raise HTTPException(status_code=404, detail="User not found.")
        return data
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/{user_id}/profile")
def update_user_profile_route(
    user_id: str,
    payload: UpdateUserProfilePayload = Body(...),
):
    try:
        return update_user_profile(user_id=user_id, profile_data=payload["profile"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{user_id}")
def delete_user_route(user_id: str):
    try:
        delete_user(user_id)
        return {"success": True}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

