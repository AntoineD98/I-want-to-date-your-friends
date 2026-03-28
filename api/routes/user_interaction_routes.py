from typing import Any, Dict, Optional, TypedDict

from fastapi import APIRouter, Body, HTTPException

from api.services.user_interaction_service import (
    approve_connection,
    create_pending_connection,
    list_connections,
    list_incoming_pending,
    list_outgoing_pending,
    record_interaction,
    remove_connection,
)


router = APIRouter(prefix="/interactions", tags=["interactions"])


class PendingConnectionPayload(TypedDict, total=False):
    endorser_id: str
    recipient_id: str
    endorsement_data: Optional[Dict[str, Any]]


class ApproveConnectionPayload(TypedDict):
    endorser_id: str
    recipient_id: str


class InteractionPayload(TypedDict, total=False):
    viewer_id: str
    target_id: str
    action: Optional[str]


@router.post("/connections/pending")
def create_pending_connection_route(
    payload: PendingConnectionPayload = Body(...),
):
    try:
        return create_pending_connection(
            endorser_id=payload.get("endorser_id", ""),
            recipient_id=payload.get("recipient_id", ""),
            endorsement_data=payload.get("endorsement_data"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/connections/approve")
def approve_connection_route(
    payload: ApproveConnectionPayload = Body(...),
):
    try:
        success = approve_connection(
            endorser_id=payload.get("endorser_id", ""),
            recipient_id=payload.get("recipient_id", ""),
        )
        return {"success": success}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/connections")
def remove_connection_route(endorser_id: str, recipient_id: str):
    try:
        success = remove_connection(endorser_id=endorser_id, recipient_id=recipient_id)
        return {"success": success}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/connections/pending/incoming/{recipient_id}")
def list_incoming_pending_route(recipient_id: str):
    try:
        return list_incoming_pending(recipient_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/connections/pending/outgoing/{endorser_id}")
def list_outgoing_pending_route(endorser_id: str):
    try:
        return list_outgoing_pending(endorser_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/connections/{user_id}")
def list_connections_route(user_id: str):
    try:
        return list_connections(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/interactions")
def record_interaction_route(
    payload: InteractionPayload = Body(...),
):
    try:
        return record_interaction(
            viewer_id=payload.get("viewer_id", ""),
            target_id=payload.get("target_id", ""),
            action=payload.get("action") or "viewed",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
