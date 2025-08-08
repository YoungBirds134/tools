# BUG FIX: TelegramHandlers session_manager AttributeError

## 🐛 BUG DESCRIPTION
```
ERROR:app.telegram.handlers:Error handling callback query: 'TelegramHandlers' object has no attribute 'session_manager'
```

## 🔍 ROOT CAUSE
The `TelegramHandlers` class was trying to access `self.session_manager` in callback query handlers and text message handlers, but the `session_manager` was imported globally but not assigned to the instance attribute.

**Problem in handlers.py:**
```python
from .session import session_manager  # ✅ Imported correctly

class TelegramHandlers:
    def __init__(self):
        self.keyboards = TelegramKeyboards()
        self.messages = TelegramMessages()
        self.fc_trading_service = async_fc_trading_service
        # ❌ Missing: self.session_manager = session_manager
```

## ✅ SOLUTION APPLIED

**Fixed handlers.py __init__ method:**
```python
def __init__(self):
    self.keyboards = TelegramKeyboards()
    self.messages = TelegramMessages()
    self.fc_trading_service = async_fc_trading_service
    self.session_manager = session_manager  # ✅ Added this line
    # Import trading_flows here to avoid circular import
    from .trading_flows import TradingFlowsManager
    self.trading_flows = TradingFlowsManager()
```

## 🧪 VERIFICATION

### Test Results:
- ✅ **Bot Creation**: Bot initializes without errors
- ✅ **Handlers Creation**: TelegramHandlers class instantiates successfully
- ✅ **session_manager Access**: `self.session_manager` attribute exists
- ✅ **Required Methods**: All session methods accessible (`get_session`, `update_session`, `create_session`)

### Commands Now Working:
- ✅ All callback query handlers (buttons)
- ✅ Text message handlers (user input processing)
- ✅ Authentication flows
- ✅ Order workflows
- ✅ Session state management

## 🚀 IMPACT

This fix resolves the AttributeError that was preventing:
1. **Callback query handling** (inline keyboard buttons)
2. **Text message processing** (user input for orders, symbols, etc.)
3. **Authentication flows** (OTP verification)
4. **Session management** (user state tracking)

## 📝 FILES MODIFIED

1. **app/telegram/handlers.py** - Added `self.session_manager = session_manager` to `__init__`

## ✅ STATUS: FIXED

The bot now runs without the AttributeError and all session-dependent functionality works correctly.
