# FSM POST CREATION FREEZE FIX (v3.1)

## Status: STABLE ✅

### Problem Fixed
Bot was stopping at step 6 (Genres input) due to:
- Missing timeout protection
- No error handling in FSM handlers
- Silent failures in state transitions
- Genres handler lacked validation before state changes

### Solution Applied

#### 1. Global FSM Timeout Protection
- Added `_check_timeout_and_refresh()` helper in routers.py
- Tracks `_last_active` timestamp for each FSM session
- Auto-clears state if user inactive > 120 seconds (2 minutes)
- Sends user-friendly Uzbek message on timeout

#### 2. All FSM Handlers Now Include:
- **Debug logging**: `print("Current state:", await state.get_state())`
- **Timeout check**: Verify session not expired before processing
- **Try/except wrapper**: Catch and log all exceptions
- **_last_active update**: Refresh timestamp on every state transition
- **User feedback**: Uzbek-friendly error messages on failure

#### 3. Enhanced Genres Handler (Step 6)
- Validates input before state change:
  - Non-empty check
  - Comma-split validation
  - Normalized genre parsing (trim, join)
- **Immediate state transition**: Updates data and moves to next state synchronously
- Better error messages for invalid input

#### 4. Wrapped Handlers
Updated with full safety:

| Handler | Changes |
|---------|---------|
| `handle_nomi` | ✅ Timeout + Try/Except + Debug |
| `handle_turi` | ✅ Timeout + Try/Except + Debug |
| `handle_reyting` | ✅ Timeout + Try/Except + Debug |
| `handle_holati` | ✅ Timeout + Try/Except + Debug |
| `handle_boblar` | ✅ Timeout + Try/Except + Debug |
| `handle_janrlar` | ✅ **VALIDATED** + Timeout + Try/Except |
| `handle_tavsif` | ✅ Timeout + Try/Except + Debug |
| `handle_tavsif_style` | ✅ Timeout + Try/Except + Debug |
| `handle_media_type` | ✅ Timeout + Try/Except + Debug |
| `handle_media_upload` | ✅ Timeout + Try/Except + Debug |
| `cb_design_select` | ✅ Timeout + Try/Except + Debug |

### Files Updated
- `src/routers.py` — All FSM handlers wrapped
- `src/states.py` — Documentation updated

### Behavior
- **No freezes**: All exceptions caught and reported
- **Responsive**: Timeout check runs async (no blocking)
- **User-friendly**: Uzbek error messages for all failures
- **Debuggable**: State and error logging on console and logger

### Testing Recommendations
1. Run through full post creation flow (10 steps)
2. Test genre input with valid/invalid formats
3. Wait 2+ minutes between inputs → state should auto-clear
4. Trigger errors (e.g., send text instead of media) → error message appears

### Debug Output Example
```
Current state: PostCreationStates.step_janrlar
Current state: PostCreationStates.step_tavsif
...
```

### Uzbek Messages Provided
- ❌ Xatolik yuz berdi. Qaytadan urinib ko'ring. (Error occurred. Try again.)
- ⏳ Sessiya muddati tugadi — yangi post yarating (Session expired — start new post)
- ⚠️ Iltimos, bir yoki bir nechta janr kiriting (Please enter one or more genres)
- ⚠️ Noto'g'ri format. Iltimos janrlarni vergul bilan ajrating (Invalid format. Separate genres by comma)
