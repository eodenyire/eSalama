"""WebSocket streaming endpoints for real-time updates"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, List
import json
from datetime import datetime

from config.database import get_db
from src.models import Student, User, UserRole

router = APIRouter(prefix="/streaming", tags=["streaming"])


# Connection manager to handle multiple WebSocket connections
class ConnectionManager:
    def __init__(self):
        # Store active connections by student_id
        self.location_connections: Dict[str, List[WebSocket]] = {}
        # Store active connections for notifications by user_id
        self.notification_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect_location(self, websocket: WebSocket, student_id: str):
        """Connect a client to location updates for a specific student"""
        await websocket.accept()
        if student_id not in self.location_connections:
            self.location_connections[student_id] = []
        self.location_connections[student_id].append(websocket)
    
    def disconnect_location(self, websocket: WebSocket, student_id: str):
        """Disconnect a client from location updates"""
        if student_id in self.location_connections:
            self.location_connections[student_id].remove(websocket)
            if not self.location_connections[student_id]:
                del self.location_connections[student_id]
    
    async def broadcast_location(self, student_id: str, message: dict):
        """Broadcast location update to all connected clients for a student"""
        if student_id in self.location_connections:
            disconnected = []
            for connection in self.location_connections[student_id]:
                try:
                    await connection.send_json(message)
                except (WebSocketDisconnect, RuntimeError, ConnectionError) as e:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                try:
                    self.location_connections[student_id].remove(conn)
                except (ValueError, KeyError):
                    pass
    
    async def connect_notifications(self, websocket: WebSocket, user_id: int):
        """Connect a client to notification updates"""
        await websocket.accept()
        if user_id not in self.notification_connections:
            self.notification_connections[user_id] = []
        self.notification_connections[user_id].append(websocket)
    
    def disconnect_notifications(self, websocket: WebSocket, user_id: int):
        """Disconnect a client from notification updates"""
        if user_id in self.notification_connections:
            self.notification_connections[user_id].remove(websocket)
            if not self.notification_connections[user_id]:
                del self.notification_connections[user_id]
    
    async def send_notification(self, user_id: int, message: dict):
        """Send notification to a specific user"""
        if user_id in self.notification_connections:
            disconnected = []
            for connection in self.notification_connections[user_id]:
                try:
                    await connection.send_json(message)
                except (WebSocketDisconnect, RuntimeError, ConnectionError) as e:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                try:
                    self.notification_connections[user_id].remove(conn)
                except (ValueError, KeyError):
                    pass


# Global connection manager instance
manager = ConnectionManager()


@router.websocket("/location/{student_id}")
async def websocket_location_stream(
    websocket: WebSocket,
    student_id: str,
    token: str = Query(..., description="JWT authentication token")
):
    """
    WebSocket endpoint for real-time location updates
    
    Clients connect and receive location updates as they happen
    
    Usage:
    - Connect: ws://localhost:8000/api/v1/streaming/location/{student_id}?token=<jwt_token>
    - Receive: JSON messages with location updates
    
    Permissions:
    - Parent: Can stream their children's locations
    - Teacher: Can stream their students' locations
    - Admin: Can stream any student's location
    """
    # Note: In a production system, you would validate the JWT token here
    # For simplicity, we're accepting connections with any token
    # TODO: Implement proper JWT validation for WebSocket connections
    
    await manager.connect_location(websocket, student_id)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection",
            "message": f"Connected to location stream for student {student_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep the connection alive and listen for messages
        while True:
            # Wait for messages from the client (e.g., ping/pong)
            data = await websocket.receive_text()
            
            # Echo back for testing
            if data == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
    except WebSocketDisconnect:
        manager.disconnect_location(websocket, student_id)
        print(f"Client disconnected from location stream for student {student_id}")


@router.websocket("/notifications")
async def websocket_notifications_stream(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token")
):
    """
    WebSocket endpoint for real-time notification updates
    
    Clients connect and receive notifications as they are sent
    
    Usage:
    - Connect: ws://localhost:8000/api/v1/streaming/notifications?token=<jwt_token>
    - Receive: JSON messages with notification updates
    
    Permissions:
    - Any authenticated user can connect to receive their notifications
    
    Note: This is a basic implementation. In production, implement proper JWT
    validation for WebSocket connections. The token should be validated and
    the user_id should be extracted from the token before establishing the connection.
    """
    # TODO: Implement JWT validation for WebSocket connections
    # Example implementation:
    # try:
    #     from src.auth.auth import decode_token
    #     payload = decode_token(token)
    #     user_id = payload.get("user_id")
    #     if not user_id:
    #         await websocket.close(code=1008)  # Policy violation
    #         return
    # except Exception:
    #     await websocket.close(code=1008)  # Policy violation
    #     return
    
    # TEMPORARY: For development/testing only
    # In production, this MUST be replaced with actual JWT validation
    user_id = 1  # Placeholder - extract from validated token in production
    
    await manager.connect_notifications(websocket, user_id)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to notification stream",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep the connection alive and listen for messages
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            
            # Echo back for testing
            if data == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
    except WebSocketDisconnect:
        manager.disconnect_notifications(websocket, user_id)
        print(f"Client disconnected from notification stream for user {user_id}")


# Helper function for other modules to broadcast location updates
async def broadcast_location_update(student_id: str, latitude: float, longitude: float, accuracy: float = None):
    """
    Broadcast location update to all connected clients
    
    This function can be called from the location_tracking module
    when a new location is recorded
    """
    message = {
        "type": "location_update",
        "student_id": student_id,
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": accuracy,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast_location(student_id, message)


# Helper function for other modules to send notifications
async def send_notification_update(user_id: int, notification_type: str, message: str, data: dict = None):
    """
    Send notification update to a specific user
    
    This function can be called from the notifications module
    when a new notification is created
    """
    notification_message = {
        "type": "notification",
        "notification_type": notification_type,
        "message": message,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.send_notification(user_id, notification_message)
