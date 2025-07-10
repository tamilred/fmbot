from pyrogram import Client, filters
from scraper import scrape_episode
import os
from dotenv import load_dotenv

load_dotenv()
bot = Client("pocketfm_bot", bot_token=os.getenv("BOT_TOKEN"))

@bot.on_message(filters.private & filters.text)
async def handle_message(client, message):
    url = message.text.strip()
    if "pocketfm.com" not in url:
        await message.reply("❌ Please send a valid Pocket FM episode URL.")
        return

    await message.reply("🔍 Scraping info...")
    result = scrape_episode(url)

    if "error" in result:
        await message.reply(f"❌ Error: {result['error']}")
    else:
        response = (
            f"🎧 **{result['title']}**\n"
            f"📖 Series: {result['series_title']}\n"
            f"✍️ Author: {result['author']}\n"
            f"📝 {result['description']}\n"
            f"📅 Uploaded: {result['uploaded']}\n"
            f"🔁 Plays: {result['plays']}\n"
        )
        await message.reply_photo(photo=result['image'], caption=response)

bot.run()
