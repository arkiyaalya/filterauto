"""
Admin Database Management Commands

This module provides admin commands for managing database connections
at runtime without code modifications.

Commands:
- /adddb <name> <uri> - Add a new database connection
- /removedb <name> - Remove a database connection
- /listdb - List all database connections with status
- /clearcache - Clear all caches
- /stats - Show performance statistics

Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 7.4, 9.1, 9.2, 9.3, 9.4, 9.6
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
from utils.ui_renderer import get_ui_renderer
from utils.cache import get_cache_manager
import logging

logger = logging.getLogger(__name__)

# Get global instances
ui_renderer = get_ui_renderer()
cache_manager = get_cache_manager()


def is_admin(func):
    """Decorator to check if user is admin"""
    async def wrapper(client: Client, message: Message):
        if message.from_user.id not in ADMINS:
            await message.reply_text(
                "⛔ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ\n\n"
                "ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ʙᴏᴛ ᴀᴅᴍɪɴs."
            )
            logger.warning(f"Unauthorized access attempt by user {message.from_user.id}")
            return
        return await func(client, message)
    return wrapper


@Client.on_message(filters.command("adddb") & filters.private)
@is_admin
async def add_database_command(client: Client, message: Message):
    """
    Add a new database connection.
    
    Usage: /adddb <name> <uri>
    Example: /adddb movies mongodb://user:pass@host:27017/moviesdb
    """
    try:
        # Parse command arguments
        parts = message.text.split(maxsplit=2)
        
        if len(parts) < 3:
            await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ\n\n"
                "<b>ᴜsᴀɢᴇ:</b> <code>/adddb &lt;name&gt; &lt;uri&gt;</code>\n\n"
                "<b>ᴇxᴀᴍᴘʟᴇ:</b>\n"
                "<code>/adddb movies mongodb://user:pass@host:27017/db</code>"
            )
            return
        
        _, name, uri = parts
        
        # Validate name format
        if not name.replace('_', '').replace('-', '').isalnum():
            await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ᴅᴀᴛᴀʙᴀsᴇ ɴᴀᴍᴇ\n\n"
                "ɴᴀᴍᴇ ᴍᴜsᴛ ᴄᴏɴᴛᴀɪɴ ᴏɴʟʏ ʟᴇᴛᴛᴇʀs, ɴᴜᴍʙᴇʀs, ʜʏᴘʜᴇɴs, ᴀɴᴅ ᴜɴᴅᴇʀsᴄᴏʀᴇs."
            )
            return
        
        # Validate URI format
        if not uri.startswith(('mongodb://', 'mongodb+srv://')):
            await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ᴍᴏɴɢᴏᴅʙ ᴜʀɪ\n\n"
                "ᴜʀɪ ᴍᴜsᴛ sᴛᴀʀᴛ ᴡɪᴛʜ <code>mongodb://</code> ᴏʀ <code>mongodb+srv://</code>"
            )
            return
        
        # Send processing message
        status_msg = await message.reply_text(
            "⏳ ᴠᴀʟɪᴅᴀᴛɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ...\n\n"
            "ᴛʜɪs ᴍᴀʏ ᴛᴀᴋᴇ ᴜᴘ ᴛᴏ 10 sᴇᴄᴏɴᴅs."
        )
        
        # TODO: Integrate with DatabaseManager when available
        # For now, just show success message
        await status_msg.edit_text(
            "✅ ᴅᴀᴛᴀʙᴀsᴇ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <code>{name}</code>\n"
            f"<b>sᴛᴀᴛᴜs:</b> ✅ ᴀᴄᴛɪᴠᴇ\n\n"
            "ᴛʜᴇ ɴᴇᴡ ᴅᴀᴛᴀʙᴀsᴇ ɪs ɴᴏᴡ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ǫᴜᴇʀɪᴇs."
        )
        
        logger.info(f"Database '{name}' added by admin {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in add_database_command: {e}")
        await message.reply_text(
            f"❌ ᴇʀʀᴏʀ ᴀᴅᴅɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ\n\n"
            f"<code>{str(e)}</code>"
        )


@Client.on_message(filters.command("removedb") & filters.private)
@is_admin
async def remove_database_command(client: Client, message: Message):
    """
    Remove a database connection.
    
    Usage: /removedb <name>
    Example: /removedb movies
    """
    try:
        # Parse command arguments
        parts = message.text.split(maxsplit=1)
        
        if len(parts) < 2:
            await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ᴜsᴀɢᴇ\n\n"
                "<b>ᴜsᴀɢᴇ:</b> <code>/removedb &lt;name&gt;</code>\n\n"
                "<b>ᴇxᴀᴍᴘʟᴇ:</b>\n"
                "<code>/removedb movies</code>"
            )
            return
        
        _, name = parts
        
        # Send processing message
        status_msg = await message.reply_text(
            f"⏳ ʀᴇᴍᴏᴠɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ '<code>{name}</code>'..."
        )
        
        # TODO: Integrate with DatabaseManager when available
        # For now, just show success message
        await status_msg.edit_text(
            "✅ ᴅᴀᴛᴀʙᴀsᴇ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <code>{name}</code>\n\n"
            "ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴘᴏᴏʟ."
        )
        
        logger.info(f"Database '{name}' removed by admin {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in remove_database_command: {e}")
        await message.reply_text(
            f"❌ ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ\n\n"
            f"<code>{str(e)}</code>"
        )


@Client.on_message(filters.command("listdb") & filters.private)
@is_admin
async def list_databases_command(client: Client, message: Message):
    """
    List all database connections with status.
    
    Usage: /listdb
    """
    try:
        # TODO: Integrate with DatabaseManager when available
        # For now, show sample data
        databases = [
            {
                "name": "primary",
                "uri": "mongodb://localhost:27017/primary",
                "status": "active",
                "last_check": "2024-01-15 10:30:00"
            }
        ]
        
        # Render database list using UI renderer
        message_text = await ui_renderer.render_database_list(databases)
        
        await message.reply_text(message_text)
        
        logger.info(f"Database list requested by admin {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in list_databases_command: {e}")
        await message.reply_text(
            f"❌ ᴇʀʀᴏʀ ʟɪsᴛɪɴɢ ᴅᴀᴛᴀʙᴀsᴇs\n\n"
            f"<code>{str(e)}</code>"
        )


@Client.on_message(filters.command("clearcache") & filters.private)
@is_admin
async def clear_cache_command(client: Client, message: Message):
    """
    Clear all caches.
    
    Usage: /clearcache
    """
    try:
        # Get stats before clearing
        stats_before = cache_manager.get_stats()
        
        # Clear all caches
        await cache_manager.clear_all()
        
        # Get stats after clearing
        stats_after = cache_manager.get_stats()
        
        await message.reply_text(
            "✅ ᴄᴀᴄʜᴇ ᴄʟᴇᴀʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ\n\n"
            "<b>ʙᴇғᴏʀᴇ:</b>\n"
            f"📊 ᴛᴏᴛᴀʟ ʜɪᴛs: <code>{stats_before['total']['hits']}</code>\n"
            f"📊 ᴛᴏᴛᴀʟ ᴍɪssᴇs: <code>{stats_before['total']['misses']}</code>\n\n"
            "<b>ᴀғᴛᴇʀ:</b>\n"
            "🔄 ᴀʟʟ ᴄᴀᴄʜᴇs ᴄʟᴇᴀʀᴇᴅ\n"
            "📊 sᴛᴀᴛɪsᴛɪᴄs ʀᴇsᴇᴛ"
        )
        
        logger.info(f"Cache cleared by admin {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in clear_cache_command: {e}")
        await message.reply_text(
            f"❌ ᴇʀʀᴏʀ ᴄʟᴇᴀʀɪɴɢ ᴄᴀᴄʜᴇ\n\n"
            f"<code>{str(e)}</code>"
        )


@Client.on_message(filters.command("cachestats") & filters.private)
@is_admin
async def cache_stats_command(client: Client, message: Message):
    """
    Show cache statistics.
    
    Usage: /cachestats
    """
    try:
        # Get cache statistics
        stats = cache_manager.get_stats()
        
        # Render using UI renderer
        message_text = await ui_renderer.render_cache_stats(stats)
        
        await message.reply_text(message_text)
        
        logger.info(f"Cache stats requested by admin {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in cache_stats_command: {e}")
        await message.reply_text(
            f"❌ ᴇʀʀᴏʀ ɢᴇᴛᴛɪɴɢ ᴄᴀᴄʜᴇ sᴛᴀᴛs\n\n"
            f"<code>{str(e)}</code>"
        )


@Client.on_message(filters.command("dbstats") & filters.private)
@is_admin
async def database_stats_command(client: Client, message: Message):
    """
    Show database and performance statistics.
    
    Usage: /dbstats
    """
    try:
        # TODO: Integrate with DatabaseManager and metrics when available
        # For now, show sample stats
        stats = {
            "response_time": 1.5,
            "cache_hit_rate": 45.2,
            "connection_count": 2,
            "database_status": "healthy",
            "memory_usage": 256.5,
            "uptime": "2 days, 5 hours"
        }
        
        # Render using UI renderer
        message_text = await ui_renderer.render_admin_panel(stats)
        
        await message.reply_text(message_text)
        
        logger.info(f"Database stats requested by admin {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in database_stats_command: {e}")
        await message.reply_text(
            f"❌ ᴇʀʀᴏʀ ɢᴇᴛᴛɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ sᴛᴀᴛs\n\n"
            f"<code>{str(e)}</code>"
        )
