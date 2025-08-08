# Session Manager for Telegram Bot
from typing import Dict, Any, Optional
import json
import time
from datetime import datetime, timedelta
import redis
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class TelegramSessionManager:
    """Session manager for Telegram bot using Redis"""
    
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.redis_url)
            self.session_timeout = settings.telegram_session_timeout_minutes * 60  # Convert to seconds
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def _get_session_key(self, chat_id: int) -> str:
        """Generate session key for a chat ID"""
        return f"telegram_session:{chat_id}"
    
    def _get_auth_key(self, chat_id: int) -> str:
        """Generate auth key for a chat ID"""
        return f"telegram_auth:{chat_id}"
    
    def create_session(self, chat_id: int, user_data: Dict[str, Any]) -> bool:
        """Create a new session for a user"""
        try:
            if not self.redis_client:
                return False
                
            session_key = self._get_session_key(chat_id)
            session_data = {
                'chat_id': chat_id,
                'created_at': time.time(),
                'last_activity': time.time(),
                'user_data': user_data,
                'authenticated': False,
                'fc_session': None
            }
            
            self.redis_client.setex(
                session_key,
                self.session_timeout,
                json.dumps(session_data)
            )
            
            logger.info(f"Session created for chat_id: {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating session for {chat_id}: {e}")
            return False
    
    def get_session(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get session data for a user"""
        try:
            if not self.redis_client:
                return None
                
            session_key = self._get_session_key(chat_id)
            session_data = self.redis_client.get(session_key)
            
            if session_data:
                return json.loads(session_data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting session for {chat_id}: {e}")
            return None
    
    def update_session(self, chat_id: int, data: Dict[str, Any]) -> bool:
        """Update session data for a user"""
        try:
            if not self.redis_client:
                return False
                
            session = self.get_session(chat_id)
            if not session:
                return False
            
            session.update(data)
            session['last_activity'] = time.time()
            
            session_key = self._get_session_key(chat_id)
            self.redis_client.setex(
                session_key,
                self.session_timeout,
                json.dumps(session)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating session for {chat_id}: {e}")
            return False
    
    def delete_session(self, chat_id: int) -> bool:
        """Delete session for a user"""
        try:
            if not self.redis_client:
                return False
                
            session_key = self._get_session_key(chat_id)
            auth_key = self._get_auth_key(chat_id)
            
            self.redis_client.delete(session_key)
            self.redis_client.delete(auth_key)
            
            logger.info(f"Session deleted for chat_id: {chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting session for {chat_id}: {e}")
            return False
    
    def is_authenticated(self, chat_id: int) -> bool:
        """Check if user is authenticated"""
        session = self.get_session(chat_id)
        return session and session.get('authenticated', False)
    
    def set_authenticated(self, chat_id: int, fc_session: Dict[str, Any]) -> bool:
        """Set user as authenticated with FC session"""
        return self.update_session(chat_id, {
            'authenticated': True,
            'fc_session': fc_session
        })
    
    def get_fc_session(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get FC session data for a user"""
        session = self.get_session(chat_id)
        if session and session.get('authenticated'):
            return session.get('fc_session')
        return None
    
    def store_temp_data(self, chat_id: int, key: str, data: Any, expire_seconds: int = 300) -> bool:
        """Store temporary data with expiration"""
        try:
            if not self.redis_client:
                return False
                
            temp_key = f"temp:{chat_id}:{key}"
            self.redis_client.setex(temp_key, expire_seconds, json.dumps(data))
            return True
            
        except Exception as e:
            logger.error(f"Error storing temp data for {chat_id}:{key}: {e}")
            return False
    
    def get_temp_data(self, chat_id: int, key: str) -> Any:
        """Get temporary data"""
        try:
            if not self.redis_client:
                return None
                
            temp_key = f"temp:{chat_id}:{key}"
            data = self.redis_client.get(temp_key)
            
            if data:
                return json.loads(data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting temp data for {chat_id}:{key}: {e}")
            return None
    
    def delete_temp_data(self, chat_id: int, key: str) -> bool:
        """Delete temporary data"""
        try:
            if not self.redis_client:
                return False
                
            temp_key = f"temp:{chat_id}:{key}"
            self.redis_client.delete(temp_key)
            return True
            
        except Exception as e:
            logger.error(f"Error deleting temp data for {chat_id}:{key}: {e}")
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions - called by background task"""
        try:
            if not self.redis_client:
                return 0
                
            # Redis automatically handles expiration, but we can do additional cleanup
            pattern = "telegram_session:*"
            keys = self.redis_client.keys(pattern)
            
            expired_count = 0
            current_time = time.time()
            
            for key in keys:
                try:
                    session_data = self.redis_client.get(key)
                    if session_data:
                        session = json.loads(session_data)
                        last_activity = session.get('last_activity', 0)
                        
                        if current_time - last_activity > self.session_timeout:
                            self.redis_client.delete(key)
                            expired_count += 1
                            
                except Exception as e:
                    logger.error(f"Error processing session key {key}: {e}")
                    
            if expired_count > 0:
                logger.info(f"Cleaned up {expired_count} expired sessions")
                
            return expired_count
            
        except Exception as e:
            logger.error(f"Error during session cleanup: {e}")
            return 0
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        try:
            if not self.redis_client:
                return 0
                
            pattern = "telegram_session:*"
            return len(self.redis_client.keys(pattern))
            
        except Exception as e:
            logger.error(f"Error getting active sessions count: {e}")
            return 0
    
    def get_active_users_count(self) -> int:
        """Get count of active users"""
        try:
            if not self.redis_client:
                return 0
            
            # Get all session keys
            session_pattern = "telegram_session:*"
            session_keys = self.redis_client.keys(session_pattern)
            
            active_count = 0
            current_time = time.time()
            
            for key in session_keys:
                try:
                    session_data = self.redis_client.get(key)
                    if session_data:
                        session = json.loads(session_data)
                        last_activity = session.get('last_activity', 0)
                        
                        # Consider user active if last activity within 1 hour
                        if current_time - last_activity < 3600:  # 1 hour
                            active_count += 1
                except:
                    continue
            
            return active_count
            
        except Exception as e:
            logger.error(f"Error getting active users count: {e}")
            return 0
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        try:
            total_sessions = self.get_active_sessions_count()
            authenticated_sessions = 0
            
            if self.redis_client:
                pattern = "telegram_session:*"
                keys = self.redis_client.keys(pattern)
                
                for key in keys:
                    try:
                        session_data = self.redis_client.get(key)
                        if session_data:
                            session = json.loads(session_data)
                            if session.get('authenticated'):
                                authenticated_sessions += 1
                    except:
                        continue
            
            return {
                'total_sessions': total_sessions,
                'authenticated_sessions': authenticated_sessions,
                'unauthenticated_sessions': total_sessions - authenticated_sessions,
                'session_timeout_minutes': settings.telegram_session_timeout_minutes
            }
            
        except Exception as e:
            logger.error(f"Error getting session stats: {e}")
            return {'error': str(e)}

# Global session manager instance
session_manager = TelegramSessionManager()
