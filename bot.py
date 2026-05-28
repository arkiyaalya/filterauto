# Modified by @Shadowedtomb and @Hail_Arka

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

from pyrogram import Client, idle
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server

from HailArka.bot import HailArkaBot
from HailArka.util.keepalive import ping_server
from HailArka.bot.clients import initialize_clients

# Import optimization modules
from database.db_manager import DatabaseManager
from utils.cache import get_cache_manager
from utils.text_formatter import TextFormatter
from utils.ui_renderer import get_ui_renderer

ppath = "plugins/*.py"
files = glob.glob(ppath)
HailArkaBot.start()
loop = asyncio.get_event_loop()


async def start():
    print('\n')
    print('Initalizing Your Bot')
    bot_info = await HailArkaBot.get_me()
    await initialize_clients()
    
    # Initialize optimization modules
    print("Initializing optimization modules...")
    
    # Initialize cache manager
    cache_manager = get_cache_manager()
    temp.CACHE = cache_manager
    print("✓ Cache Manager initialized")
    
    # Initialize database manager
    db_manager = DatabaseManager()
    await db_manager.load_config()
    db_manager.start_health_check()
    temp.DB_MANAGER = db_manager
    print("✓ Database Manager initialized")
    
    # Initialize UI renderer and text formatter
    ui_renderer = get_ui_renderer()
    temp.UI_RENDERER = ui_renderer
    temp.TEXT_FORMATTER = TextFormatter()
    print("✓ UI Renderer and Text Formatter initialized")
    
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("ShadowedTombbotz Imported => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    elif ON_KOYEB or ON_RENDER:
        asyncio.create_task(ping_server())  # Enable keep-alive for Koyeb and Render too
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    me = await HailArkaBot.get_me()
    temp.BOT = HailArkaBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    try:
        await HailArkaBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except:
        print("Make Your Bot Admin In Log Channel With Full Rights")
    for ch in CHANNELS:
        try:
            k = await HailArkaBot.send_message(chat_id=ch, text="**Bot Restarted**")
            await k.delete()
        except:
            print("Make Your Bot Admin In File Channels With Full Rights")
    try:
        k = await HailArkaBot.send_message(chat_id=AUTH_CHANNEL, text="**Bot Restarted**")
        await k.delete()
    except:
        print("Make Your Bot Admin In Force Subscribe Channel With Full Rights")
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')


