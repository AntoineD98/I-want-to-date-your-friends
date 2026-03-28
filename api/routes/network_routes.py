from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from api.services.network_service import get_discovery_feed


router = APIRouter(prefix="/network", tags=["network"])


@router.get("/discovery/{user_id}")
def get_network_discovery(
    user_id: str,
    start_at: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    action: Optional[str] = None,
):
    """
    Return a paginated discovery feed for the given user.
    """
    try:
        return get_discovery_feed(
            viewer_id=user_id,
            start_at=start_at,
            limit=limit,
            action=action,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

