import time
import os
import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

SEND_TIMES = ["20:00", "22:00"]
sent_today = set()

bot = Bot(token=TOKEN)

async def send_bell():
    if not os.path.exists("bell.ogg"):
        print("bell.ogg not found!")
        return
    
    voice_msg = await bot.send_voice(
        chat_id=GROUP_ID,
        voice=open("bell.ogg", "rb")
    )
    
    await bot.send_message(
        chat_id=GROUP_ID,
        text="🙏 રાધે કૃષ્ણ 🙏"
    )
    
    try:
        await bot.pin_chat_message(
            chat_id=GROUP_ID,
            message_id=voice_msg.message_id
        )
    except:
        pass


while True:
    now = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%Y-%m-%d")
    
    for t in SEND_TIMES:
        key = f"{today}_{t}"
        
        if now == t and key not in sent_today:
            asyncio.run(send_bell())
            sent_today.add(key)
    
    if now == "00:01":
        sent_today.clear()
    
    time.sleep(20)
