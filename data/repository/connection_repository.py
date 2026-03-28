from sqlmodel import select, or_, and_
from typing import Dict, List, Optional, Set
from data.db.session import get_session
from data.sql_model.user import User
from data.sql_model.connection import Connection

#contains functions for managing the network of users and their connections, including adding users, creating endorsements, and generating discovery feeds based on the network of connections.
class ConnectionRepository:
    def __init__(self, session):
        self.session = session

    def get_direct_connections(self, user_id: str) -> Set[str]:
        statement = select(Connection).where(
            or_(Connection.endorser_id == user_id, Connection.recipient_id == user_id)
        )
        results = self.session.exec(statement).all()
        
        connections = set()
        for connection in results:
            connections.add(connection.recipient_id if connection.endorser_id == user_id else connection.endorser_id)
        return connections

    #returns a dict of user_ids that are one connection away from the given user_id, along with the set of direct connections that connect them to the given user_id
    def get_discovery_network(self, user_id: str) -> Optional[Dict[str, List[str]]]:
        
        connections = self.get_direct_connections(user_id)
        if not connections:
            return {}

        discovery_network = {str: Set[str]}()

        for connection_id in connections:
            connection_connections = self.get_direct_connections(connection_id)
            
            for connection_connection_id in connection_connections:
                if connection_connection_id != user_id and connection_connection_id not in connections:
                    connection_connection = self.session.get(User, connection_connection_id)
                    if connection_connection and not connection_connection.node_only:
                        if connection_connection_id not in discovery_network:
                            discovery_network[connection_connection_id] = set(connection_id)
                        else:
                            discovery_network[connection_connection_id].add(connection_id)
        
        return discovery_network
    
    def get_names_from_ids(self, user_ids: list[str]) -> dict[str, str]:
        statement = select(User.user_id, User.name).where(User.user_id.in_(user_ids))
        results = self.session.exec(statement).all()
        return {user_id: name for user_id, name in results}
    
    #contains data for paginated discovery feed
    def get_feed(self, discovery_network: dict[str, Set[str]], start_at: int = 0, limit: int = 10) -> Dict:
        feed = []
        connected_ids = set()

        #sanitize start_at and limit
        start_at = max(0, min(start_at, len(discovery_network)))
        limit = min(start_at + limit, len(discovery_network))
        target_ids = list(discovery_network.keys())[start_at : start_at + limit]

        if len(target_ids) == 0:
            return {
                "feed": [],
                "next": None,
                "total": len(discovery_network) 
            }

        #store list of all connected ids for query
        for id in target_ids:
            connected_ids.update(discovery_network[id])

        statement = select(User).where(
            and_(User.user_id.in_(target_ids), User.node_only == False)
            )
        results = self.session.exec(statement).all()
        connected_users = self.get_names_from_ids(list(connected_ids))
        for user in results:
            feed.append({
                "user": user,
                "connected_by": [connected_users[conn_id] for conn_id in discovery_network[user.user_id]]
            })

        return {
            "feed": feed,
            "next": start_at + limit if start_at + limit < len(discovery_network) else None,
            "network": discovery_network
        }
