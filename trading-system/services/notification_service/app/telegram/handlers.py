"""
Enhanced Telegram handlers for notification service
Production-ready handlers with comprehensive notification support
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Dict, Any, Optional
import json
import asyncio
from datetime import datetime

from ..core.config import settings
from ..models.telegram_models import TelegramUserState
from ..models.notification_models import NotificationType, NotificationPriority
from .session import SessionManager
from .keyboards import TelegramKeyboards, TelegramMessages
from .utils import is_authorized_user, format_currency
from ..services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class TelegramHandlers:
    """Enhanced handlers for all Telegram bot commands and interactions"""
    
    def __init__(self):
        self.keyboards = TelegramKeyboards()
        self.messages = TelegramMessages()
        self.session_manager = SessionManager()
        self.notification_service = NotificationService()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command with enhanced welcome flow"""
        try:
            chat_id = update.effective_chat.id
            user = update.effective_user
            
            logger.info(f"Start command received from chat_id: {chat_id}")
            
            # Check if user is authorized
            if not is_authorized_user(chat_id):
                await update.message.reply_text(
                    "❌ **Access Denied**\n\n"
                    "You are not authorized to use this notification service.\n"
                    "Please contact your administrator for access.",
                    parse_mode='Markdown'
                )
                return
            
            # Create or update session
            user_data = {
                'chat_id': chat_id,
                'username': user.username or 'Unknown',
                'first_name': user.first_name or 'User',
                'last_name': user.last_name or '',
                'language_code': user.language_code or 'en',
                'last_activity': datetime.now(),
                'state': TelegramUserState.START
            }
            
            session = self.session_manager.create_session(chat_id, user_data)
            logger.info(f"Session created/updated for user: {user.first_name} ({chat_id})")
            
            # Send enhanced welcome message
            welcome_text = f"""
🚀 **Welcome to Trading Notification Service**

👋 Hello {user.first_name}!

I'm your professional trading notification bot. I'll keep you informed about:

📊 **Trading Updates**
• Order executions and fills
• Price and volume alerts
• Market open/close notifications

💰 **Account Monitoring**
• Balance changes
• Margin calls and risk alerts
• Portfolio performance updates

🔔 **System Notifications**
• Maintenance windows
• Security alerts
• Service status updates

**🎯 Quick Actions:**
• Use the menu buttons below to get started
• Type /help for detailed command list
• Type /settings to configure your preferences

*Ready to stay informed about your trading activities!*
"""
            
            try:
                await update.message.reply_text(
                    welcome_text,
                    reply_markup=self.keyboards.start_keyboard(),
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
                
                # Log successful start
                await self.notification_service.send_notification(
                    user_id=str(chat_id),
                    notification_type=NotificationType.SYSTEM_MAINTENANCE,
                    title="User Started Bot",
                    message=f"User {user.first_name} ({user.username}) started the notification bot",
                    priority=NotificationPriority.LOW
                )
                
            except Exception as send_error:
                logger.error(f"Error sending welcome message: {send_error}")
                await update.message.reply_text(
                    "✅ Welcome to Trading Notification Service!\n"
                    "Use /help for available commands."
                )
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            try:
                await update.message.reply_text(
                    "❌ An error occurred during initialization. Please try again."
                )
            except:
                pass
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command with comprehensive help"""
        try:
            chat_id = update.effective_chat.id
            
            if not is_authorized_user(chat_id):
                await update.message.reply_text("❌ Access denied.")
                return
            
            help_text = """
📚 **Notification Service Help**

**🔔 Notification Commands:**
/start - Initialize the bot and show welcome
/help - Show this help message
/menu - Show main menu
/status - Check service status
/settings - Configure notification preferences
/subscribe - Subscribe to notifications
/unsubscribe - Unsubscribe from notifications

**📊 Information Commands:**
/notifications - View recent notifications
/alerts - Manage price and volume alerts
/account - View account notification settings
/stats - View notification statistics

**⚙️ Configuration Commands:**
/quiet_hours - Set quiet hours (no notifications)
/priority - Set minimum notification priority
/channels - Configure notification channels
/templates - Manage notification templates

**🆘 Support Commands:**
/support - Contact support team
/feedback - Send feedback
/report - Report an issue

**💡 Quick Tips:**
• Use buttons in menus for easier navigation
• Set quiet hours to avoid night notifications
• Configure priority levels to filter important alerts
• Use /status to check if all services are running

**🔗 Related Services:**
• Trading Service: Port 8000
• Market Data: Port 8002
• Notification Service: Port 8001

Need more help? Contact support or check the documentation.
"""
            
            await update.message.reply_text(
                help_text,
                reply_markup=self.keyboards.help_menu(),
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /menu command"""
        try:
            chat_id = update.effective_chat.id
            
            if not is_authorized_user(chat_id):
                await update.message.reply_text("❌ Access denied.")
                return
            
            # Update session state
            self.session_manager.update_session_state(chat_id, TelegramUserState.MAIN_MENU)
            
            menu_text = """
🏠 **Main Menu**

Welcome to the Trading Notification Service control panel.
Choose an option below to manage your notifications and settings.

📊 **Current Status**: All services operational
🔔 **Active Notifications**: Enabled
⚡ **Last Update**: Just now
"""
            
            await update.message.reply_text(
                menu_text,
                reply_markup=self.keyboards.main_menu(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in menu command: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command - show service status"""
        try:
            chat_id = update.effective_chat.id
            
            if not is_authorized_user(chat_id):
                await update.message.reply_text("❌ Access denied.")
                return
            
            # Get service status
            status_info = await self.notification_service.get_service_status()
            
            status_text = f"""
🔍 **Service Status Report**

**📊 Notification Service**
Status: {'🟢 Online' if status_info.get('notification_service') else '🔴 Offline'}
Uptime: {status_info.get('uptime', 'Unknown')}
Queue: {status_info.get('queue_size', 0)} pending

**💬 Telegram Bot**
Status: {'�� Connected' if status_info.get('telegram_bot') else '🔴 Disconnected'}
Messages Today: {status_info.get('messages_sent_today', 0)}
Last Message: {status_info.get('last_message_time', 'Unknown')}

**��️ Database**
Status: {'🟢 Connected' if status_info.get('database') else '🔴 Disconnected'}
Notifications Stored: {status_info.get('total_notifications', 0)}

**🔄 External Services**
Trading Service: {'🟢 Available' if status_info.get('trading_service') else '🔴 Unavailable'}
Market Data: {'🟢 Available' if status_info.get('market_data') else '🔴 Unavailable'}

**⏰ Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            await update.message.reply_text(
                status_text,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text(
                "❌ Unable to fetch service status. Please try again later."
            )
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle all callback queries from inline keyboards"""
        try:
            query = update.callback_query
            await query.answer()
            
            chat_id = update.effective_chat.id
            user_id = update.effective_user.id
            data = query.data
            
            logger.info(f"Callback query received: {data} from chat_id: {chat_id}")
            
            # Check authorization
            if not is_authorized_user(chat_id):
                await query.edit_message_text("❌ Access denied.")
                return
            
            # Handle different callback types
            result = await self._handle_callback_data(data, chat_id, user_id)
            
            if result:
                try:
                    if result.get('keyboard'):
                        await query.edit_message_text(
                            result['message'],
                            reply_markup=result['keyboard'],
                            parse_mode='Markdown'
                        )
                    else:
                        await query.edit_message_text(
                            result['message'],
                            parse_mode='Markdown'
                        )
                except Exception as edit_error:
                    if "Message is not modified" not in str(edit_error):
                        logger.error(f"Error editing message: {edit_error}")
                        # Send new message instead
                        await query.message.reply_text(
                            result['message'],
                            reply_markup=result.get('keyboard'),
                            parse_mode='Markdown'
                        )
            
        except Exception as e:
            logger.error(f"Error handling callback query: {e}")
            try:
                await update.callback_query.edit_message_text(
                    "❌ An error occurred. Please try again."
                )
            except:
                pass
    
    async def _handle_callback_data(self, data: str, chat_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Handle specific callback data"""
        try:
            # Main menu navigation
            if data == "main_menu":
                return {
                    'success': True,
                    'message': "🏠 **Main Menu**\n\nChoose an option:",
                    'keyboard': self.keyboards.main_menu()
                }
            
            elif data == "notifications_menu":
                return {
                    'success': True,
                    'message': "🔔 **Notifications Menu**\n\nManage your notifications:",
                    'keyboard': self.keyboards.notifications_menu()
                }
            
            elif data == "settings_menu":
                return {
                    'success': True,
                    'message': "⚙️ **Settings Menu**\n\nConfigure your preferences:",
                    'keyboard': self.keyboards.settings_menu()
                }
            
            elif data == "help_menu":
                return {
                    'success': True,
                    'message': "❓ **Help Menu**\n\nGet help and support:",
                    'keyboard': self.keyboards.help_menu()
                }
            
            # Notification management
            elif data == "view_notifications":
                notifications = await self.notification_service.get_user_notifications(str(chat_id))
                return await self._format_notifications_response(notifications)
            
            elif data == "notification_settings":
                settings_info = await self.notification_service.get_user_settings(str(chat_id))
                return await self._format_settings_response(settings_info)
            
            elif data == "subscribe_all":
                await self.notification_service.subscribe_user(str(chat_id))
                return {
                    'success': True,
                    'message': "✅ **Subscribed Successfully**\n\nYou will now receive all notifications.",
                    'keyboard': self.keyboards.notifications_menu()
                }
            
            elif data == "unsubscribe_all":
                await self.notification_service.unsubscribe_user(str(chat_id))
                return {
                    'success': True,
                    'message': "🔕 **Unsubscribed Successfully**\n\nYou will no longer receive notifications.",
                    'keyboard': self.keyboards.notifications_menu()
                }
            
            # Default handler for unknown callbacks
            else:
                return {
                    'success': True,
                    'message': f"ℹ️ **Feature Coming Soon**\n\nThe feature '{data}' is under development.",
                    'keyboard': self.keyboards.main_menu()
                }
                
        except Exception as e:
            logger.error(f"Error handling callback data '{data}': {e}")
            return {
                'success': False,
                'message': "❌ An error occurred processing your request.",
                'keyboard': self.keyboards.main_menu()
            }
    
    async def _format_notifications_response(self, notifications: list) -> Dict[str, Any]:
        """Format notifications list for display"""
        if not notifications:
            return {
                'success': True,
                'message': "📭 **No Notifications**\n\nYou have no recent notifications.",
                'keyboard': self.keyboards.notifications_menu()
            }
        
        message = "🔔 **Recent Notifications**\n\n"
        for notif in notifications[:10]:  # Show last 10
            status_emoji = "✅" if notif['status'] == 'delivered' else "⏳"
            message += f"{status_emoji} **{notif['title']}**\n"
            message += f"📅 {notif['created_at']}\n"
            message += f"💬 {notif['message'][:100]}...\n\n"
        
        return {
            'success': True,
            'message': message,
            'keyboard': self.keyboards.notifications_menu()
        }
    
    async def _format_settings_response(self, settings_info: dict) -> Dict[str, Any]:
        """Format user settings for display"""
        message = f"""
⚙️ **Your Notification Settings**

**🔔 Status**: {'Enabled' if settings_info.get('enabled', True) else 'Disabled'}
**📱 Channels**: {', '.join(settings_info.get('channels', ['Telegram']))}
**🎯 Min Priority**: {settings_info.get('min_priority', 'Normal').title()}
**🌙 Quiet Hours**: {settings_info.get('quiet_hours', 'Not set')}
**🌍 Timezone**: {settings_info.get('timezone', 'UTC')}

**📊 Statistics Today**:
• Messages received: {settings_info.get('messages_today', 0)}
• Alerts triggered: {settings_info.get('alerts_today', 0)}
• Last notification: {settings_info.get('last_notification', 'None')}
"""
        
        return {
            'success': True,
            'message': message,
            'keyboard': self.keyboards.settings_menu()
        }
