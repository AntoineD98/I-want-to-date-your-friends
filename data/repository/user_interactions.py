from sqlmodel import Session, create_engine, select, or_, and_
from typing import Any, Dict, List, Optional, Set

from data.sql_model.connection import Connection, PendingConnection
from data.sql_model.interaction import Interaction, ActionType


#contains functions for managing user interactions, including sending connection requests, accepting or rejecting requests, and blocking users.
class UserInteractionsRepository:
    def __init__(self, session):
        self.session=session

    def add_pending_connection(self, pending_connection: PendingConnection) -> bool:
        self.session.add(pending_connection)
        self.session.commit()
        return True
    
    def get_pending_connection(self, endorser_id: str, recipient_id: str) -> Optional[PendingConnection]:
        statement = select(PendingConnection).where(
            and_(PendingConnection.endorser_id == endorser_id,
            PendingConnection.recipient_id == recipient_id
            )
        )
        pending_connection = self.session.exec(statement).first()
        return pending_connection
    
    def get_incomming_pending_connections(self, recipient_id: str) -> List[PendingConnection]:
        statement = select(PendingConnection).where(
            PendingConnection.recipient_id == recipient_id
        )
        pending_connections = self.session.exec(statement).all()
        return pending_connections
    
    def get_outgoing_pending_connections(self, endorser_id: str) -> List[PendingConnection]:
        statement = select(PendingConnection).where(
            PendingConnection.endorser_id == endorser_id
        )
        pending_connections = self.session.exec(statement).all()
        return pending_connections
    
    def approve_connection(self, pending_connection: PendingConnection) -> bool:
        statement = select(PendingConnection).where(
            and_(PendingConnection.endorser_id == pending_connection.endorser_id,
            PendingConnection.recipient_id == pending_connection.recipient_id
            )
        )
        pending_connection = self.session.exec(statement).first()
        if pending_connection:
            new_connection = Connection(**pending_connection.model_dump(exclude={"id"}))
            self.session.add(new_connection)
            self.session.delete(pending_connection)
            self.session.commit()
            return True
        return False

    def get_connection(self, endorser_id: str, recipient_id: str) -> Optional[Connection]:
        statement = select(Connection).where(
            and_(Connection.endorser_id == endorser_id,
            Connection.recipient_id == recipient_id
            )
        )
        connection = self.session.exec(statement).first()
        return connection
    
    def get_connections(self, user_id: str) -> List[Connection]:
        statement = select(Connection).where(Connection.recipient_id == user_id)
        results = self.session.exec(statement).all()
        return results

    def remove_connection(self, endorser_id: str, recipient_id: str) -> bool:
        statement = select(Connection).where(
            Connection.endorser_id == endorser_id,
            Connection.recipient_id == recipient_id
        )
        connection = self.session.exec(statement).first()
        if connection:
            self.session.delete(connection)
            self.session.commit()
            return True
        return False
    
    def remove_connections(self, user_id: str) -> bool:
        statement = select(Connection).where(
            or_(Connection.endorser_id == user_id, Connection.recipient_id == user_id)
        )
        results = self.session.exec(statement).all()
        for connection in results:
            self.session.delete(connection)
        statement = select(PendingConnection).where(
            or_(PendingConnection.endorser_id == user_id, PendingConnection.recipient_id == user_id)
        )
        results = self.session.exec(statement).all()
        for pending_connection in results:
            self.session.delete(pending_connection)
        self.session.commit()
        return True
        
    def get_interaction(self, viewer_id: str, target_id: str) -> Optional[Interaction]:
        statement = select(Interaction).where(
            and_(Interaction.viewer_id == viewer_id,
            Interaction.target_id == target_id
            )
        )
        interaction = self.session.exec(statement).first()
        return interaction

    def add_interaction(self, interaction: Interaction) -> bool:
        if interaction.action not in ActionType.__members__:
            return False  # Invalid action type
        self.session.add(interaction)
        self.session.commit()
        return True
        
    #filters by action type, if action is None, filters for uninteracted users
    def filter_discovery_network_by_interaction(self, viewer_id: str, discovery_network: Dict[str, Set[str]], action: ActionType = None) -> Dict[str, Set[str]]:
        if not action:
            statement= select(Interaction).where(Interaction.viewer_id == viewer_id)
        else:
            statement = select(Interaction).where(
                and_(Interaction.viewer_id == viewer_id,
                Interaction.action == action)
            )
        interactions = self.session.exec(statement).all()
        interacted_ids = {interaction.target_id for interaction in interactions}
        if not action:
            filtered_network = {user_id: connections for user_id, connections in discovery_network.items() if user_id not in interacted_ids}
        else:
            filtered_network = {user_id: connections for user_id, connections in discovery_network.items() if user_id in interacted_ids}
        return filtered_network
