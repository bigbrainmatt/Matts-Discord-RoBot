import threading
from api import run_api
from bot import run_bot
import asyncio

threading.Thread(target=run_api, daemon=True).start()
asyncio.run(run_bot())