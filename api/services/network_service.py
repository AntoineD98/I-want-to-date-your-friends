from typing import Dict, Optional, Set

from data.repository.connection_repository import Network
from data.repository.user_interactions import UserInteractions
from data.sql_model.interaction import ActionType
from data.sql_model.user import User


network = Network()
user_interactions = UserInteractions()

class NetworkService:
    def __init__(self):
        self.cache


def get_feed(user_id: str,
             interaction: ActionType = None,
             next: int = 0,
             discovery_network: Dict[str, Set[str]] = None) -> Dict[User, Set[str]]:
    if not user_id:
        raise ValueError("user_id is required.")

    if discovery_network is None:
        discovery_network = Network.get_discovery_network(user_id)
    discovery_network = network.get_one_connection_away(user_id)
    return discovery_network or {}


def get_filtered_discovery_network(
    viewer_id: str,
    action: Optional[str] = None,
) -> Dict[str, Set[str]]:
    """
    Return the discovery network optionally filtered by prior interaction.
    If action is None, returns only users the viewer has not yet interacted with.
    """
    base_network = get_discovery_network(viewer_id)
    if not base_network:
        return {}

    action_type: Optional[ActionType]
    if action is None:
        action_type = None
    else:
        try:
            action_type = ActionType(action)
        except ValueError:
            raise ValueError(f"Invalid action type: {action}")

    return user_interactions.filter_discovery_network_by_interaction(
        viewer_id=viewer_id,
        discovery_network=base_network,
        action=action_type,
    )


def get_discovery_feed(
    viewer_id: str,
    start_at: int = 0,
    limit: int = 10,
    action: Optional[str] = None,
) -> Dict:
    """
    Build a paginated discovery feed for a viewer, optionally filtered by interaction type.
    Returns a dict with "feed", "next", "total"; each feed item has "user" (dict) and "connected_by" (list).
    """
    if start_at < 0:
        raise ValueError("start_at must be non-negative.")
    if limit <= 0:
        raise ValueError("limit must be positive.")

    filtered_network = get_filtered_discovery_network(viewer_id, action=action)
    return network.get_feed_serialized(
        filtered_network, start_at=start_at, limit=limit
    )

