# Telegram Admin Posting System - Production Build

## Architecture

Single-router FSM-based bot for posting media to Telegram channels with full entity preservation.

## Entry Points

- `run.py` - Bot startup and dispatcher configuration
- `post_create.py` - All FSM handlers and post creation logic

## FSM Flow

```
/start or "📚 POST YARATISH"
    ↓ (state: waiting_media)
User sends photo/video
    ↓ (state: waiting_caption)
Bot asks for caption text
    ↓ (state: waiting_link)
User sends caption (entities preserved)
Bot asks for link
    ↓ (state: waiting_button_text)
User sends link
Bot asks for button text
    ↓ (state: waiting_confirm)
User sends button text
Bot builds preview (send_photo/send_video with caption_entities)
Bot shows confirm/cancel
    ↓
User selects confirm
Bot calls copy_message(preview → channel with keyboard)
Bot clears state
Bot shows main menu
```

## Key Features

1. **Caption Entity Preservation**
   - Saves `message.entities` when caption is received
   - Passes `caption_entities` to preview send
   - Preserves blockquote frames, formatting, emojis, spacing

2. **Message Replication**
   - Preview message is captured with message_id
   - Confirm handler uses `copy_message()` only
   - No rebuild, no parsing, no formatting

3. **State Management**
   - Linear FSM with 5 states
   - State clears after confirm or cancel
   - Main menu re-shown after publish
   - No overlapping handlers

4. **Error Handling**
   - Structured logging (INFO level)
   - Try/except in all handlers
   - User-facing error messages
   - Graceful fallbacks

## Configuration

Required `.env` variables:
- `BOT_TOKEN` - Telegram bot token
- `PUBLISH_CHANNELS` - Channel IDs (comma-separated, first used)

## Data Flow

```
Media received
  ↓
Save: media_type, file_id

Caption received
  ↓
Save: caption, caption_entities

Link received
  ↓
Save: url

Button text received
  ↓
Save: button_text
Build preview (send_photo/send_video)
Save: preview_chat_id, preview_message_id
Show confirm keyboard
  ↓
Confirm:
  Copy preview to channel with keyboard
  Clear state
  Show main menu
```

## State Data Schema

```python
{
    'media_type': 'photo' | 'video',
    'file_id': str,
    'caption': str,
    'caption_entities': list,
    'url': str,
    'button_text': str,
    'preview_chat_id': int,
    'preview_message_id': int
}
```

## Handlers

- `start_command()` - /start
- `start_post_flow()` - "📚 POST YARATISH" button
- `handle_photo()/handle_video()` - Media input
- `handle_caption()` - Caption text with entities
- `handle_link()` - URL validation and storage
- `handle_button_text()` - Button text, builds preview
- `confirm()` - Publishes via copy_message
- `cancel()` - Clears state, shows menu

## Testing

1. Start bot: `py -3.11 run.py`
2. Send /start
3. Press "📚 POST YARATISH"
4. Send photo/video
5. Send caption with blockquote (use > prefix in Telegram)
6. Send link (http://...)
7. Send button text
8. Confirm → post appears in channel with exact formatting
9. Main menu shows again

## Production Notes

- Single instance only (Telegram API constraint)
- MemoryStorage (resets on restart; use Redis for production)
- No database persistence
- All state in FSM context
- Logs to console at INFO level
- Error details logged; safe messages to user

## Entity Preservation Chain

1. User sends caption with blockquote → `message.entities` captured
2. Bot stores `caption_entities = message.entities`
3. Preview sent: `send_photo(caption_entities=caption_entities)`
4. Telegram attaches entities to preview message
5. Confirm copies preview: `copy_message()` preserves all entities
6. Channel message identical to preview

## No-Rebuild Policy

- ✗ Never use `parse_mode`
- ✗ Never extract and reconstruct caption
- ✗ Never modify text
- ✗ Never remove entities
- ✗ Never call `send_photo` on confirm (fallback removed)
- ✓ Always use `copy_message` for channel publish
- ✓ Always pass `caption_entities` to preview
- ✓ Always preserve user's original formatting
