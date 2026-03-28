from typing import Any, Dict, List, Optional

from data.sql_interface.user_interactions import UserInteractions


user_interactions = UserInteractions()


def create_pending_connection(
    endorser_id: str,
    recipient_id: str,
    endorsement_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not endorser_id or not recipient_id:
        raise ValueError("endorser_id and recipient_id are required.")
    if endorser_id == recipient_id:
        raise ValueError("endorser_id and recipient_id must be different.")

    pending = user_interactions.create_pending_connection_from_data(
        endorser_id=endorser_id,
        recipient_id=recipient_id,
        endorsement_data=endorsement_data,
    )
    if not pending:
        raise ValueError("A pending connection or connection already exists.")
    return pending.model_dump()


def approve_connection(endorser_id: str, recipient_id: str) -> bool:
    if not endorser_id or not recipient_id:
        raise ValueError("endorser_id and recipient_id are required.")

    pending = user_interactions.get_pending_connection(endorser_id, recipient_id)
    if not pending:
        raise ValueError("No pending connection found to approve.")

    return user_interactions.approve_connection(pending)


def remove_connection(endorser_id: str, recipient_id: str) -> bool:
    if not endorser_id or not recipient_id:
        raise ValueError("endorser_id and recipient_id are required.")
    return user_interactions.remove_connection(endorser_id, recipient_id)


def list_incoming_pending(recipient_id: str) -> List[Dict[str, Any]]:
    if not recipient_id:
        raise ValueError("recipient_id is required.")
    items = user_interactions.get_incomming_pending_connections(recipient_id)
    return [p.model_dump() for p in items]


def list_outgoing_pending(endorser_id: str) -> List[Dict[str, Any]]:
    if not endorser_id:
        raise ValueError("endorser_id is required.")
    items = user_interactions.get_outgoing_pending_connections(endorser_id)
    return [p.model_dump() for p in items]


def list_connections(user_id: str) -> List[Dict[str, Any]]:
    if not user_id:
        raise ValueError("user_id is required.")
    items = user_interactions.get_connections(user_id)
    return [c.model_dump() for c in items]


def record_interaction(
    viewer_id: str, target_id: str, action: str
) -> Dict[str, Any]:
    if not viewer_id or not target_id:
        raise ValueError("viewer_id and target_id are required.")

    interaction = user_interactions.add_interaction_from_data(
        viewer_id=viewer_id,
        target_id=target_id,
        action=action,
    )
    if not interaction:
        raise ValueError(f"Invalid action type: {action}")
    return interaction.model_dump()

