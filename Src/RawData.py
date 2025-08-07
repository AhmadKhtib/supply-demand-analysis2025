import telethon
import re
from telethon import TelegramClient
from datetime import datetime, timezone
import nest_asyncio
import asyncio
import pandas as pd
import json


nest_asyncio.apply()
# Load configuration from JSON file
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']
channel_id = config['channel_id']
# Initialize the Telegram client

client = TelegramClient('session_name', api_id, api_hash)
messages= dict()
async def main():
    await client.start()
    print(" Connected to Telegram")
    channel = await client.get_entity(channel_id)
    # Make dates timezone-aware (UTC)
    start_date = datetime(2025,8 , 2, 14, 59, 59, tzinfo=timezone.utc)
    end_date = datetime(2025, 8 , 6, 12, 59, 59, tzinfo=timezone.utc)

    count = 0
    async for msg in client.iter_messages(channel, 
                                          offset_date=end_date,
                                            reverse=False):
        if start_date <= msg.date <= end_date:
            if msg.text:
                print(f"[{msg.date}] {msg.sender_id}: {msg.text}")
                messages[msg.date]=msg.text
                count += 1

    print(f"\n Total plain text messages between {start_date.date()} and {end_date.date()} is : {count}")
    await client.disconnect()

asyncio.run(main())

# Save messages dict to CSV with date and text columns
df = pd.DataFrame(list(messages.items()), columns=["date", "text"])
df.to_csv(r"Data\RawData02.csv", index=False, encoding="utf-8-sig")