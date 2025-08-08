"""
Telegram Bot Utilities
Helper functions for formatting and validation
"""

import re
from functools import wraps
from typing import Optional, Dict, Any, List
from datetime import datetime
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
import logging

logger = logging.getLogger(__name__)


def format_currency(amount: float, currency: str = "VND") -> str:
    """Format currency amount with proper formatting"""
    try:
        if currency == "VND":
            return f"{amount:,.0f} ₫"
        elif currency == "USD":
            return f"${amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"
    except (ValueError, TypeError):
        return "0 ₫"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage with proper sign and color indicator"""
    try:
        sign = "+" if value >= 0 else ""
        emoji = "📈" if value >= 0 else "📉"
        return f"{emoji} {sign}{value:.{decimals}f}%"
    except (ValueError, TypeError):
        return "0.00%"


def format_number(value: float, decimals: int = 0) -> str:
    """Format number with thousand separators"""
    try:
        return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return "0"


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object"""
    try:
        return dt.strftime(format_str)
    except (ValueError, AttributeError):
        return datetime.now().strftime(format_str)


def validate_stock_symbol(symbol: str) -> bool:
    """Validate Vietnamese stock symbol format"""
    if not symbol:
        return False
    
    # Vietnamese stock symbols are typically 3-4 characters, all uppercase
    pattern = r'^[A-Z]{3,4}$'
    return bool(re.match(pattern, symbol.upper()))


def validate_price(price_str: str) -> Optional[float]:
    """Validate and parse price string"""
    try:
        # Remove commas and convert to float
        price = float(price_str.replace(",", ""))
        
        # Price must be positive
        if price <= 0:
            return None
            
        # Price should be reasonable (not too high/low)
        if price > 1000000000 or price < 0.1:
            return None
            
        return price
    except (ValueError, TypeError):
        return None


def validate_quantity(quantity_str: str) -> Optional[int]:
    """Validate and parse quantity string"""
    try:
        # Remove commas and convert to int
        quantity = int(quantity_str.replace(",", ""))
        
        # Quantity must be positive
        if quantity <= 0:
            return None
            
        # Quantity should be reasonable
        if quantity > 100000000:  # 100 million shares max
            return None
            
        return quantity
    except (ValueError, TypeError):
        return None


def validate_order_data(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate complete order data"""
    errors = []
    
    # Required fields
    required_fields = ['instrument_id', 'price', 'quantity', 'buy_sell', 'order_type']
    for field in required_fields:
        if field not in order_data or order_data[field] is None:
            errors.append(f"Missing required field: {field}")
    
    # Validate stock symbol
    if 'instrument_id' in order_data:
        if not validate_stock_symbol(order_data['instrument_id']):
            errors.append("Invalid stock symbol format")
    
    # Validate price
    if 'price' in order_data:
        try:
            price = float(order_data['price'])
            if price <= 0:
                errors.append("Price must be positive")
        except (ValueError, TypeError):
            errors.append("Invalid price format")
    
    # Validate quantity
    if 'quantity' in order_data:
        try:
            quantity = int(order_data['quantity'])
            if quantity <= 0:
                errors.append("Quantity must be positive")
        except (ValueError, TypeError):
            errors.append("Invalid quantity format")
    
    # Validate buy_sell
    if 'buy_sell' in order_data:
        if order_data['buy_sell'] not in ['B', 'S']:
            errors.append("buy_sell must be 'B' or 'S'")
    
    # Validate order_type
    if 'order_type' in order_data:
        if order_data['order_type'] not in ['LO', 'MP', 'ATO', 'ATC']:
            errors.append("Invalid order type")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }


def send_typing_action(func):
    """Decorator to send typing action before function execution"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            # Send typing action
            if update.effective_chat:
                await context.bot.send_chat_action(
                    chat_id=update.effective_chat.id,
                    action=ChatAction.TYPING
                )
            
            # Execute the function
            return await func(update, context, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    
    return wrapper


def escape_markdown(text: str) -> str:
    """Escape special characters for Markdown"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def truncate_text(text: str, max_length: int = 4000) -> str:
    """Truncate text to fit Telegram message limits"""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at a word boundary
    truncated = text[:max_length - 3]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length // 2:  # If we can find a reasonable word boundary
        return truncated[:last_space] + "..."
    else:
        return truncated + "..."


def format_order_status(status: str) -> str:
    """Format order status with appropriate emoji"""
    status_map = {
        'PENDING': '⏳ Pending',
        'FILLED': '✅ Filled',
        'PARTIALLY_FILLED': '🔄 Partially Filled',
        'CANCELLED': '❌ Cancelled',
        'REJECTED': '🚫 Rejected',
        'EXPIRED': '⏰ Expired'
    }
    
    return status_map.get(status, f'❓ {status}')


def format_order_type(order_type: str) -> str:
    """Format order type with description"""
    type_map = {
        'LO': 'Limit Order',
        'MP': 'Market Price',
        'ATO': 'At The Opening',
        'ATC': 'At The Close'
    }
    
    return type_map.get(order_type, order_type)


def format_buy_sell(buy_sell: str) -> str:
    """Format buy/sell with appropriate emoji"""
    if buy_sell == 'B':
        return '🛒 Buy'
    elif buy_sell == 'S':
        return '🛍️ Sell'
    else:
        return f'❓ {buy_sell}'


def calculate_order_value(price: float, quantity: int) -> float:
    """Calculate total order value"""
    return price * quantity


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100


def is_market_open() -> bool:
    """Check if market is currently open"""
    now = datetime.now()
    current_time = now.time()
    
    # Vietnamese market hours: 9:00 AM - 3:00 PM (Monday to Friday)
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    from datetime import time
    market_open = time(9, 0)
    market_close = time(15, 0)
    
    return market_open <= current_time <= market_close


def is_authorized_user(chat_id: int) -> bool:
    """Check if user is authorized to use the bot"""
    try:
        from ..config import settings
        
        # If no restrictions set, allow all users
        if not hasattr(settings, 'telegram_allowed_chat_ids') or not settings.telegram_allowed_chat_ids:
            return True
        
        # Check if user is in allowed list
        return str(chat_id) in settings.telegram_allowed_chat_ids
        
    except Exception as e:
        logger.error(f"Error checking user authorization: {e}")
        return False


def validate_symbol(symbol: str) -> bool:
    """Validate Vietnamese stock symbol"""
    try:
        if not symbol:
            return False
        
        # Remove whitespace and convert to uppercase
        symbol = symbol.strip().upper()
        
        # Vietnamese stock symbols are typically 3-4 characters
        if len(symbol) < 2 or len(symbol) > 5:
            return False
        
        # Should contain only letters and numbers
        if not re.match(r'^[A-Z0-9]+$', symbol):
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating symbol: {e}")
        return False


def get_market_status() -> Dict[str, Any]:
    """Get current market status"""
    try:
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        
        # Vietnamese market hours: 9:00 AM - 3:00 PM, Monday to Friday
        market_open_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        market_close_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        
        # Check if it's a weekday
        is_weekday = now.weekday() < 5  # Monday = 0, Friday = 4
        
        # Check if within market hours
        is_within_hours = market_open_time <= now <= market_close_time
        
        is_open = is_weekday and is_within_hours
        
        if is_open:
            next_session = "Market is currently open"
            message = "Trading session is active"
        elif is_weekday and now < market_open_time:
            next_session = f"Market opens at 09:00"
            message = "Market will open soon"
        elif is_weekday and now > market_close_time:
            next_session = "Market opens tomorrow at 09:00"
            message = "Market is closed for today"
        else:
            next_session = "Market opens Monday at 09:00"
            message = "Market is closed for weekend"
        
        return {
            'is_open': is_open,
            'current_time': current_time,
            'next_session': next_session,
            'message': message
        }
        
    except Exception as e:
        logger.error(f"Error getting market status: {e}")
        return {
            'is_open': False,
            'current_time': datetime.now().strftime('%H:%M:%S'),
            'next_session': 'Unknown',
            'message': 'Unable to determine market status'
        }


def format_price_change(current_price: float, previous_price: float) -> str:
    """Format price change with color and percentage"""
    if previous_price == 0:
        return "N/A"
    
    change = current_price - previous_price
    change_pct = (change / previous_price) * 100
    
    if change > 0:
        return f"📈 +{change:,.0f} (+{change_pct:.2f}%)"
    elif change < 0:
        return f"📉 {change:,.0f} ({change_pct:.2f}%)"
    else:
        return f"➖ 0 (0.00%)"


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\']', '', text)
    
    return text


def validate_chat_permissions(user_id: int, required_permissions: List[str] = None) -> bool:
    """Validate if user has required permissions"""
    from ..config import settings
    
    # Check if user is in allowed list
    try:
        allowed_ids = eval(settings.telegram_allowed_chat_ids)
        if str(user_id) not in allowed_ids:
            return False
    except:
        pass
    
    # Add additional permission checks here
    return True


def log_user_action(user_id: int, action: str, details: Dict[str, Any] = None):
    """Log user action for auditing"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'action': action,
        'details': details or {}
    }
    
    logger.info(f"User action: {log_entry}")


def generate_order_summary(order_data: Dict[str, Any]) -> str:
    """Generate a formatted order summary"""
    try:
        action = format_buy_sell(order_data.get('buy_sell', ''))
        symbol = order_data.get('instrument_id', 'N/A')
        price = format_currency(order_data.get('price', 0))
        quantity = format_number(order_data.get('quantity', 0))
        total = format_currency(calculate_order_value(
            order_data.get('price', 0),
            order_data.get('quantity', 0)
        ))
        order_type = format_order_type(order_data.get('order_type', ''))
        
        return f"""
**Order Summary**

{action} {symbol}
Price: {price}
Quantity: {quantity:,}
Total: {total}
Type: {order_type}
"""
    except Exception as e:
        logger.error(f"Error generating order summary: {str(e)}")
        return "Error generating order summary"


def create_pagination_keyboard(current_page: int, total_pages: int, callback_prefix: str) -> List[List]:
    """Create pagination keyboard for large datasets"""
    keyboard = []
    
    # Navigation buttons
    nav_buttons = []
    
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"{callback_prefix}_{current_page - 1}"))
    
    nav_buttons.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="noop"))
    
    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{callback_prefix}_{current_page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    return keyboard
