from sqlmodel import Session, create_engine, select, or_, and_
from typing import Any, Dict, List, Optional, Set

from data.sql_model.connection import Connection, PendingConnection
from data.sql_model.interaction import Interaction, ActionType


#contains functions for managing user interactions, including sending connection requests, accepting or rejecting requests, and blocking users.
class UserInteractions:
    def __init__(self, db_url: str = "sqlite:///database.db"):
        self.engine = create_engine(db_url)
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(self.engine)

    def add_pending_connection(self, pending_connection: PendingConnection) -> bool:
        with Session(self.engine) as session:
            session.add(pending_connection)
            session.commit()
            return True
    
    def get_pending_connection(self, endorser_id: str, recipient_id: str) -> Optional[PendingConnection]:
        with Session(self.engine) as session:
            statement = select(PendingConnection).where(
                and_(PendingConnection.endorser_id == endorser_id,
                PendingConnection.recipient_id == recipient_id
                )
            )
            pending_connection = session.exec(statement).first()
            return pending_connection
    
    def get_incomming_pending_connections(self, recipient_id: str) -> List[PendingConnection]:
        with Session(self.engine) as session:
            statement = select(PendingConnection).where(
                PendingConnection.recipient_id == recipient_id
            )
            pending_connections = session.exec(statement).all()
            return pending_connections
    
    def get_outgoing_pending_connections(self, endorser_id: str) -> List[PendingConnection]:
        with Session(self.engine) as session:
            statement = select(PendingConnection).where(
                PendingConnection.endorser_id == endorser_id
            )
            pending_connections = session.exec(statement).all()
            return pending_connections
    
    def approve_connection(self, pending_connection: PendingConnection) -> bool:
        with Session(self.engine) as session:
            statement = select(PendingConnection).where(
                and_(PendingConnection.endorser_id == pending_connection.endorser_id,
                PendingConnection.recipient_id == pending_connection.recipient_id
                )
            )
            pending_connection = session.exec(statement).first()
            if pending_connection:
                new_connection = Connection(**pending_connection.model_dump(exclude={"id"}))
                session.add(new_connection)
                session.delete(pending_connection)
                session.commit()
                return True
            return False

    def get_connection(self, endorser_id: str, recipient_id: str) -> Optional[Connection]:
        with Session(self.engine) as session:
            statement = select(Connection).where(
                and_(Connection.endorser_id == endorser_id,
                Connection.recipient_id == recipient_id
                )
            )
            connection = session.exec(statement).first()
            return connection
    
    def get_connections(self, user_id: str) -> List[Connection]:
        with Session(self.engine) as session:
            statement = select(Connection).where(Connection.recipient_id == user_id)
            results = session.exec(statement).all()
            return results

    def remove_connection(self, endorser_id: str, recipient_id: str) -> bool:
        with Session(self.engine) as session:
            statement = select(Connection).where(
                Connection.endorser_id == endorser_id,
                Connection.recipient_id == recipient_id
            )
            connection = session.exec(statement).first()
            if connection:
                session.delete(connection)
                session.commit()
                return True
            return False
    
    def remove_connections(self, user_id: str) -> bool:
        with Session(self.engine) as session:
            statement = select(Connection).where(
                or_(Connection.endorser_id == user_id, Connection.recipient_id == user_id)
            )
            results = session.exec(statement).all()
            for connection in results:
                session.delete(connection)
            statement = select(PendingConnection).where(
                or_(PendingConnection.endorser_id == user_id, PendingConnection.recipient_id == user_id)
            )
            results = session.exec(statement).all()
            for pending_connection in results:
                session.delete(pending_connection)
            session.commit()
        return True
        
    def get_interaction(self, viewer_id: str, target_id: str) -> Optional[Interaction]:
        with Session(self.engine) as session:
            statement = select(Interaction).where(
                and_(Interaction.viewer_id == viewer_id,
                Interaction.target_id == target_id
                )
            )
            interaction = session.exec(statement).first()
            return interaction

    def add_interaction(self, interaction: Interaction) -> bool:
        with Session(self.engine) as session:
            if interaction.action not in ActionType.__members__:
                return False  # Invalid action type
            session.add(interaction)
            session.commit()
            return True
        
    #filters by action type, if action is None, filters for uninteracted users
    def filter_discovery_network_by_interaction(self, viewer_id: str, discovery_network: Dict[str, Set[str]], action: ActionType = None) -> Dict[str, Set[str]]:
        with Session(self.engine) as session:
            if not action:
                statement= select(Interaction).where(Interaction.viewer_id == viewer_id)
            else:
                statement = select(Interaction).where(
                    and_(Interaction.viewer_id == viewer_id,
                    Interaction.action == action)
                )
            interactions = session.exec(statement).all()
            interacted_ids = {interaction.target_id for interaction in interactions}
            if not action:
                filtered_network = {user_id: connections for user_id, connections in discovery_network.items() if user_id not in interacted_ids}
            else:
                filtered_network = {user_id: connections for user_id, connections in discovery_network.items() if user_id in interacted_ids}
            return filtered_network

    def create_pending_connection_from_data(
        self,
        endorser_id: str,
        recipient_id: str,
        endorsement_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[PendingConnection]:
        """Create and persist a pending connection. Returns None if one already exists."""
        if self.get_pending_connection(endorser_id, recipient_id):
            return None
        if self.get_connection(endorser_id, recipient_id):
            return None
        pending = PendingConnection(
            endorser_id=endorser_id,
            recipient_id=recipient_id,
            endorsement_data=endorsement_data,
        )
        self.add_pending_connection(pending)
        return pending

    def add_interaction_from_data(
        self, viewer_id: str, target_id: str, action: str
    ) -> Optional[Interaction]:
        """Create and persist an interaction. Returns None if action is invalid."""
        try:
            action_type = ActionType(action)
        except ValueError:
            return None
        interaction = Interaction(
            viewer_id=viewer_id,
            target_id=target_id,
            action=action_type,
        )
        if not self.add_interaction(interaction):
            return None
        return interaction

