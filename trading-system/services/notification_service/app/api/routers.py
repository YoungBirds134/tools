"""
FastAPI routers for notification service
RESTful API endpoints for notification management
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from ..core.config import settings
from ..models.notification_models import (
    NotificationType, 
    NotificationPriority, 
    NotificationChannel
)
from ..services.notification_service import NotificationService

logger = logging.getLogger(__name__)

# Initialize routers
notifications_router = APIRouter(prefix="/notifications", tags=["notifications"])
users_router = APIRouter(prefix="/users", tags=["users"])
health_router = APIRouter(prefix="/health", tags=["health"])

# Dependency injection
def get_notification_service():
    return NotificationService()


# Pydantic models for API
class NotificationRequest(BaseModel):
    user_id: str
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    channels: Optional[List[NotificationChannel]] = None
    metadata: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None


class NotificationResponse(BaseModel):
    success: bool
    notification_id: Optional[str] = None
    status: Optional[str] = None
    delivery_results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Notification endpoints
@notifications_router.post("/send", response_model=NotificationResponse)
async def send_notification(
    request: NotificationRequest,
    service: NotificationService = Depends(get_notification_service)
):
    """Send a notification to a user"""
    try:
        logger.info(f"Sending notification to user {request.user_id}: {request.title}")
        
        result = await service.send_notification(
            user_id=request.user_id,
            notification_type=request.notification_type,
            title=request.title,
            message=request.message,
            priority=request.priority,
            channels=request.channels,
            metadata=request.metadata,
            scheduled_at=request.scheduled_at
        )
        
        return NotificationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@notifications_router.get("/{user_id}", response_model=List[Dict[str, Any]])
async def get_user_notifications(
    user_id: str,
    limit: int = 20,
    service: NotificationService = Depends(get_notification_service)
):
    """Get recent notifications for a user"""
    try:
        notifications = await service.get_user_notifications(user_id, limit)
        return notifications
        
    except Exception as e:
        logger.error(f"Error getting user notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# User management endpoints  
@users_router.get("/{user_id}/settings", response_model=Dict[str, Any])
async def get_user_settings(
    user_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """Get user notification settings"""
    try:
        settings = await service.get_user_settings(user_id)
        return settings
        
    except Exception as e:
        logger.error(f"Error getting user settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.post("/{user_id}/subscribe", response_model=Dict[str, Any])
async def subscribe_user(
    user_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """Subscribe user to notifications"""
    try:
        success = await service.subscribe_user(user_id)
        
        if success:
            return {'success': True, 'message': 'User subscribed successfully'}
        else:
            raise HTTPException(status_code=500, detail="Failed to subscribe user")
            
    except Exception as e:
        logger.error(f"Error subscribing user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.post("/{user_id}/unsubscribe", response_model=Dict[str, Any])
async def unsubscribe_user(
    user_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """Unsubscribe user from notifications"""
    try:
        success = await service.unsubscribe_user(user_id)
        
        if success:
            return {'success': True, 'message': 'User unsubscribed successfully'}
        else:
            raise HTTPException(status_code=500, detail="Failed to unsubscribe user")
            
    except Exception as e:
        logger.error(f"Error unsubscribing user: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoints
@health_router.get("/")
async def health_check(
    service: NotificationService = Depends(get_notification_service)
):
    """Get comprehensive service health status"""
    try:
        status = await service.get_service_status()
        return status
        
    except Exception as e:
        logger.error(f"Error getting service status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@health_router.get("/live")
async def liveness_probe():
    """Simple liveness probe for Kubernetes"""
    return {"status": "alive", "timestamp": datetime.now().isoformat()}


# Test endpoints
@notifications_router.post("/test/{user_id}")
async def send_test_notification(
    user_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """Send test notification to verify service is working"""
    try:
        result = await service.send_notification(
            user_id=user_id,
            notification_type=NotificationType.SYSTEM_MAINTENANCE,
            title="🧪 Test Notification",
            message="This is a test notification to verify the service is working correctly.",
            priority=NotificationPriority.LOW
        )
        
        return {'success': True, 'message': 'Test notification sent', 'result': result}
        
    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))
