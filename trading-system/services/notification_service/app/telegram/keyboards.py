"""
Telegram Bot Keyboards and Messages
Enhanced keyboards for comprehensive trading flows
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from typing import List, Dict, Any, Optional
import json
from ..config import settings
from .models import TelegramUserState, OrderStatus, MarketStatus
from .utils import format_currency, get_market_status


class TelegramKeyboards:
    """Telegram inline keyboards for trading flows"""
    
    @staticmethod
    def start_keyboard() -> InlineKeyboardMarkup:
        """Start/Welcome keyboard with initial options"""
        keyboard = [
            [
                InlineKeyboardButton("🚀 Get Started", callback_data="main_menu"),
                InlineKeyboardButton("❓ Help", callback_data="help_menu")
            ],
            [
                InlineKeyboardButton("🔐 Login", callback_data="auth_login"),
                InlineKeyboardButton("📊 Market Status", callback_data="market_status")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Main menu keyboard with all available options"""
        keyboard = []
        
        # Core trading features
        if settings.enable_trading_commands:
            keyboard.append([
                InlineKeyboardButton("⚡ Trading", callback_data="trade_menu"),
                InlineKeyboardButton("� Portfolio", callback_data="portfolio_menu")
            ])
        
        # Market data and information
        if settings.enable_market_data:
            keyboard.append([
                InlineKeyboardButton("� Market Data", callback_data="market_menu"),
                InlineKeyboardButton("📈 Charts", callback_data="charts_menu")
            ])
        
        # Alerts and notifications
        if settings.enable_alerts_notifications:
            keyboard.append([
                InlineKeyboardButton("🔔 Alerts", callback_data="alerts_menu"),
                InlineKeyboardButton("📰 News", callback_data="news_menu")
            ])
        
        # Legacy authentication menu
        keyboard.append([
            InlineKeyboardButton("� Authentication", callback_data="auth_menu"),
            InlineKeyboardButton("👤 Account", callback_data="account_menu")
        ])
        
        # Help and support
        keyboard.append([
            InlineKeyboardButton("❓ Help", callback_data="help_menu"),
            InlineKeyboardButton("📞 Support", callback_data="support_menu")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def auth_menu() -> InlineKeyboardMarkup:
        """Authentication menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📱 Get OTP", callback_data="get_otp"),
                InlineKeyboardButton("🔑 Verify Code", callback_data="verify_code")
            ],
            [
                InlineKeyboardButton("🔍 Check Token", callback_data="check_token"),
                InlineKeyboardButton("🚪 Logout", callback_data="logout")
            ],
            [
                InlineKeyboardButton("⬅️ Back to Main", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_menu() -> InlineKeyboardMarkup:
        """Order menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📈 New Stock Order", callback_data="new_stock_order"),
                InlineKeyboardButton("📉 New Derivative Order", callback_data="new_derivative_order")
            ],
            [
                InlineKeyboardButton("✏️ Modify Order", callback_data="modify_order"),
                InlineKeyboardButton("❌ Cancel Order", callback_data="cancel_order")
            ],
            [
                InlineKeyboardButton("📋 Order History", callback_data="order_history"),
                InlineKeyboardButton("📖 Order Book", callback_data="order_book")
            ],
            [
                InlineKeyboardButton("⬅️ Back to Main", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def account_menu() -> InlineKeyboardMarkup:
        """Account menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Stock Balance", callback_data="stock_balance"),
                InlineKeyboardButton("💎 Derivative Balance", callback_data="derivative_balance")
            ],
            [
                InlineKeyboardButton("📊 Stock Position", callback_data="stock_position"),
                InlineKeyboardButton("📈 Derivative Position", callback_data="derivative_position")
            ],
            [
                InlineKeyboardButton("⚡ PP/MMR Info", callback_data="pp_mmr_info"),
                InlineKeyboardButton("🔢 Max Quantities", callback_data="max_quantities")
            ],
            [
                InlineKeyboardButton("⬅️ Back to Main", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def help_menu() -> InlineKeyboardMarkup:
        """Help menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📚 User Guide", callback_data="user_guide"),
                InlineKeyboardButton("🎯 Quick Start", callback_data="quick_start")
            ],
            [
                InlineKeyboardButton("⚙️ Commands List", callback_data="commands_list"),
                InlineKeyboardButton("🆘 Contact Support", callback_data="contact_support")
            ],
            [
                InlineKeyboardButton("⬅️ Back to Main", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def market_selection() -> InlineKeyboardMarkup:
        """Market selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🏛️ Stock Market (VN)", callback_data="market_VN"),
                InlineKeyboardButton("📊 Derivative Market (VNFE)", callback_data="market_VNFE")
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="order_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def buy_sell_selection() -> InlineKeyboardMarkup:
        """Buy/Sell selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📈 Buy (B)", callback_data="buysell_B"),
                InlineKeyboardButton("📉 Sell (S)", callback_data="buysell_S")
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="order_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_type_selection() -> InlineKeyboardMarkup:
        """Order type selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🎯 Limit Order (LO)", callback_data="ordertype_LO"),
                InlineKeyboardButton("⚡ Market Order (MP)", callback_data="ordertype_MP")
            ],
            [
                InlineKeyboardButton("🌅 ATO Order", callback_data="ordertype_ATO"),
                InlineKeyboardButton("🌅 ATC Order", callback_data="ordertype_ATC")
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="order_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirmation_keyboard(action: str, data: str = "") -> InlineKeyboardMarkup:
        """Confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{action}_{data}"),
                InlineKeyboardButton("❌ Cancel", callback_data="order_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def pagination_keyboard(current_page: int, total_pages: int, action: str) -> InlineKeyboardMarkup:
        """Pagination keyboard"""
        keyboard = []
        
        # Navigation buttons
        nav_buttons = []
        if current_page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"{action}_page_{current_page-1}"))
        if current_page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{action}_page_{current_page+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Page info
        keyboard.append([InlineKeyboardButton(f"Page {current_page+1}/{total_pages}", callback_data="noop")])
        
        # Back button
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_to_main() -> InlineKeyboardMarkup:
        """Simple back to main menu keyboard"""
        keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def cancel_operation() -> InlineKeyboardMarkup:
        """Cancel current operation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("❌ Cancel", callback_data="main_menu"),
                InlineKeyboardButton("🔄 Try Again", callback_data="restart")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def trading_menu() -> InlineKeyboardMarkup:
        """Trading menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🛒 Buy Order", callback_data="trade_buy"),
                InlineKeyboardButton("🛍️ Sell Order", callback_data="trade_sell")
            ],
            [
                InlineKeyboardButton("📋 Order History", callback_data="trade_history"),
                InlineKeyboardButton("⏰ Pending Orders", callback_data="trade_pending")
            ],
            [
                InlineKeyboardButton("🔄 Modify Order", callback_data="trade_modify"),
                InlineKeyboardButton("❌ Cancel Order", callback_data="trade_cancel")
            ],
            [
                InlineKeyboardButton("📊 Order Book", callback_data="trade_orderbook"),
                InlineKeyboardButton("💹 Price Quote", callback_data="trade_quote")
            ]
        ]
        
        if settings.telegram_enable_stop_loss:
            keyboard.append([
                InlineKeyboardButton("🛑 Stop Loss", callback_data="trade_stop_loss"),
                InlineKeyboardButton("🎯 Take Profit", callback_data="trade_take_profit")
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def portfolio_menu() -> InlineKeyboardMarkup:
        """Portfolio menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Balance", callback_data="portfolio_balance"),
                InlineKeyboardButton("📊 Holdings", callback_data="portfolio_stocks")
            ],
            [
                InlineKeyboardButton("💹 Derivatives", callback_data="portfolio_derivatives"),
                InlineKeyboardButton("📈 P&L Summary", callback_data="portfolio_pnl")
            ],
            [
                InlineKeyboardButton("📋 History", callback_data="portfolio_history"),
                InlineKeyboardButton("📊 Performance", callback_data="portfolio_performance")
            ]
        ]
        
        if settings.telegram_enable_portfolio_analytics:
            keyboard.append([
                InlineKeyboardButton("📈 Analytics", callback_data="portfolio_analytics"),
                InlineKeyboardButton("📊 Risk Analysis", callback_data="portfolio_risk")
            ])
        
        keyboard.extend([
            [InlineKeyboardButton("🔄 Refresh", callback_data="portfolio_refresh")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def market_data_menu() -> InlineKeyboardMarkup:
        """Market data menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Overview", callback_data="market_overview"),
                InlineKeyboardButton("🏢 Indices", callback_data="market_indices")
            ],
            [
                InlineKeyboardButton("🔥 Top Gainers", callback_data="market_gainers"),
                InlineKeyboardButton("📉 Top Losers", callback_data="market_losers")
            ],
            [
                InlineKeyboardButton("💰 Most Active", callback_data="market_active"),
                InlineKeyboardButton("📊 Market Depth", callback_data="market_depth")
            ]
        ]
        
        if settings.telegram_enable_technical_analysis:
            keyboard.append([
                InlineKeyboardButton("📈 Technical Analysis", callback_data="market_technical"),
                InlineKeyboardButton("📊 Indicators", callback_data="market_indicators")
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def alerts_menu() -> InlineKeyboardMarkup:
        """Alerts menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🔔 Price Alert", callback_data="alert_create_price"),
                InlineKeyboardButton("📊 Volume Alert", callback_data="alert_create_volume")
            ],
            [
                InlineKeyboardButton("📋 Active Alerts", callback_data="alert_list_active"),
                InlineKeyboardButton("📜 Alert History", callback_data="alert_history")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="alert_settings"),
                InlineKeyboardButton("🔕 Disable All", callback_data="alert_disable_all")
            ]
        ]
        
        if settings.telegram_enable_market_open_alert:
            keyboard.append([
                InlineKeyboardButton("🌅 Market Open Alert", callback_data="alert_market_open"),
                InlineKeyboardButton("🌇 Market Close Alert", callback_data="alert_market_close")
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_type_selection() -> InlineKeyboardMarkup:
        """Order type selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Limit Order", callback_data="order_type_LO"),
                InlineKeyboardButton("🚀 Market Order", callback_data="order_type_MP")
            ],
            [
                InlineKeyboardButton("🌅 At Opening", callback_data="order_type_ATO"),
                InlineKeyboardButton("🌇 At Closing", callback_data="order_type_ATC")
            ],
            [InlineKeyboardButton("❌ Cancel", callback_data="trade_menu")]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_confirmation(order_data: Dict[str, Any]) -> InlineKeyboardMarkup:
        """Order confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm & Submit", callback_data="order_submit"),
                InlineKeyboardButton("✏️ Edit", callback_data="order_edit")
            ],
            [InlineKeyboardButton("❌ Cancel", callback_data="trade_menu")]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def enhanced_back_to_main() -> InlineKeyboardMarkup:
        """Enhanced back to main menu keyboard"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ])
    
    @staticmethod
    def enhanced_cancel_keyboard(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
        """Enhanced cancel operation keyboard"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data=callback_data)]
        ])
    
    @staticmethod
    def yes_no_keyboard(yes_callback: str, no_callback: str) -> InlineKeyboardMarkup:
        """Yes/No confirmation keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Yes", callback_data=yes_callback),
                InlineKeyboardButton("❌ No", callback_data=no_callback)
            ]
        ])
    
    @staticmethod
    def settings_menu() -> InlineKeyboardMarkup:
        """Settings menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications"),
                InlineKeyboardButton("🎨 Display", callback_data="settings_display")
            ],
            [
                InlineKeyboardButton("🔐 Security", callback_data="settings_security"),
                InlineKeyboardButton("⚡ Trading", callback_data="settings_trading")
            ],
            [
                InlineKeyboardButton("🌐 Language", callback_data="settings_language"),
                InlineKeyboardButton("🕒 Timezone", callback_data="settings_timezone")
            ],
            [
                InlineKeyboardButton("🔄 Reset Settings", callback_data="settings_reset"),
                InlineKeyboardButton("📤 Export Data", callback_data="settings_export")
            ],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def enhanced_help_menu() -> InlineKeyboardMarkup:
        """Enhanced help menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📖 User Guide", callback_data="help_guide"),
                InlineKeyboardButton("❓ FAQ", callback_data="help_faq")
            ],
            [
                InlineKeyboardButton("🎯 Trading Tips", callback_data="help_tips"),
                InlineKeyboardButton("⚡ Quick Start", callback_data="help_quickstart")
            ],
            [
                InlineKeyboardButton("📞 Contact Support", callback_data="help_support"),
                InlineKeyboardButton("🐛 Report Bug", callback_data="help_bug")
            ],
            [
                InlineKeyboardButton("📋 Commands", callback_data="help_commands"),
                InlineKeyboardButton("🔄 What's New", callback_data="help_changelog")
            ],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
        
        return InlineKeyboardMarkup(keyboard)
    

class TelegramMessages:
    """Static messages for the bot"""
    
    WELCOME_MESSAGE = """
🤖 **Welcome to FC Trading Bot!**

I'm your personal trading assistant for SSI FastConnect Trading.

🔹 **Features:**
• Real-time order management
• Account balance & positions
• Trading history
• Market data

🔹 **Getting Started:**
1. Authenticate with your SSI account
2. Start trading with simple commands
3. Get real-time updates

Use the menu below to navigate 👇
"""
    
    AUTH_REQUIRED = """
🔐 **Authentication Required**

Please authenticate with your SSI FastConnect account first.

1. Click "Get OTP" to receive verification code
2. Enter the code when prompted
3. Start trading!
"""
    
    HELP_MESSAGE = """
🆘 **FC Trading Bot Help**

**📱 Commands:**
• `/start` - Start the bot
• `/help` - Show this help
• `/menu` - Show main menu
• `/status` - Check your status
• `/logout` - Logout from FC account

**🔹 Quick Actions:**
• Authentication & OTP verification
• Place buy/sell orders
• Check account balances
• View trading positions
• Order history & management

**⚠️ Important:**
• Keep your credentials secure
• Always verify order details
• Contact support for issues

**🆘 Need Help?**
Contact support: support@example.com
"""
    
    ERROR_MESSAGE = """
❌ **Error Occurred**

Something went wrong. Please try again later.

If the problem persists, contact support.
"""
    
    SUCCESS_MESSAGE = """
✅ **Operation Successful**

Your request has been processed successfully.
"""
    
    # Enhanced Trading Flow Messages
    WELCOME_MESSAGE = """
🎉 **Welcome to FC Trading Bot!**

Your professional trading assistant for Vietnamese stock market.

🔥 **What you can do:**
• 📊 View real-time market data
• 💰 Check your portfolio
• ⚡ Place buy/sell orders
• 🔔 Set price alerts
• 📈 Get market insights

🚀 **Getting Started:**
1. Set up your FC account
2. Login to authenticate
3. Start trading!

Choose an option below to begin:
"""
    
    TRADING_HELP_MESSAGE = """
📊 **Trading Help**

**Order Types:**
• 📊 **Limit Order (LO)**: Buy/sell at specific price
• 🚀 **Market Order (MP)**: Buy/sell at current market price
• 🌅 **At Opening (ATO)**: Execute at market opening
• 🌇 **At Closing (ATC)**: Execute at market closing

**Tips:**
• Check your balance before placing orders
• Review order details carefully
• Set price alerts for better timing
• Monitor your positions regularly

**Market Hours:**
Monday - Friday: 9:00 AM - 3:00 PM
"""
    
    PORTFOLIO_HELP_MESSAGE = """
💼 **Portfolio Help**

**Available Information:**
• 💰 Account balance and buying power
• 📊 Stock holdings and positions
• 💹 Derivative positions
• 📈 Profit & Loss summary
• 📋 Transaction history

**Features:**
• Real-time portfolio valuation
• Performance analytics
• Risk assessment
• Position tracking

**Refresh Data:**
Click "Refresh" to get latest information.
"""
    
    ALERTS_HELP_MESSAGE = """
🔔 **Alerts Help**

**Alert Types:**
• 🔔 **Price Alert**: Notify when price reaches target
• 📊 **Volume Alert**: Notify on volume changes
• 🌅 **Market Open**: Daily market opening notification
• 🌇 **Market Close**: Daily market closing notification

**Setting Alerts:**
1. Choose alert type
2. Enter stock symbol
3. Set target price/volume
4. Confirm alert creation

**Managing Alerts:**
• View active alerts
• Disable/enable alerts
• Delete alerts
• Alert history
"""
    
    MARKET_CLOSED_MESSAGE = """
🔴 **Market is Currently Closed**

Trading hours: Monday - Friday, 9:00 AM - 3:00 PM

You can still:
• 📊 View market data
• 💼 Check your portfolio
• 🔔 Set price alerts
• 📈 Analyze charts

Orders will be processed when market reopens.
"""
    
    ORDER_SUCCESS_MESSAGE = """
✅ **Order Submitted Successfully!**

Your order has been sent to the market and will be processed according to market rules.

You can track your order status in the "Pending Orders" section.
"""
    
    ORDER_FAILED_MESSAGE = """
❌ **Order Failed**

Your order could not be processed. Please check:
• Account balance
• Order parameters
• Market status
• Stock availability

Try again or contact support if the problem persists.
"""
    
    FEATURE_DISABLED_MESSAGE = """
🚫 **Feature Disabled**

This feature is currently disabled by the administrator.

Please contact support for more information.
"""
    
    @staticmethod
    def get_market_status_message() -> str:
        """Get current market status message"""
        status = get_market_status()
        
        if status['is_open']:
            return f"""
🟢 **Market is Open**

Current time: {status['current_time']}
Trading session is active.

All trading features are available.
"""
        else:
            return f"""
🔴 **Market is Closed**

Current time: {status['current_time']}
Next trading session: Tomorrow 9:00 AM

Limited features available during market close.
"""
    
    @staticmethod
    def get_order_summary_message(order_data: Dict[str, Any]) -> str:
        """Get order summary message"""
        action = "Buy" if order_data.get('buy_sell') == 'B' else "Sell"
        symbol = order_data.get('instrument_id', 'N/A')
        price = format_currency(order_data.get('price', 0))
        quantity = order_data.get('quantity', 0)
        total = format_currency(order_data.get('price', 0) * order_data.get('quantity', 0))
        
        return f"""
📋 **Order Summary**

**Action:** {action}
**Symbol:** {symbol}
**Price:** {price}
**Quantity:** {quantity:,} shares
**Total Value:** {total}

⚠️ Please review carefully before confirming.
"""
