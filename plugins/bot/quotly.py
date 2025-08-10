import os
import random
import aiohttp
from io import BytesIO
from pyrogram import filters
from ChampuMusic import app
from pyrogram.types import Message

# List warna yang tersedia
QUOTE_COLORS = [
    "black", "white", "blue", "green", "red", "pink",
    "purple", "orange", "grey", "brown"
]

# API Quotly
QUOTLY_API = "https://bot.lyo.su/quote/generate.png"

async def generate_quote(messages, color, is_reply=False):
    """
    Kirim data ke API Quotly dan return file BytesIO stiker.
    """
    payload = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": color,
        "messages": []
    }

    for msg in messages:
        if not msg.from_user:
            continue

        # Data reply
        reply_data = None
        if is_reply and msg.reply_to_message and msg.reply_to_message.from_user:
            reply_data = {
                "name": msg.reply_to_message.from_user.first_name or "NoName",
                "username": msg.reply_to_message.from_user.username or "",
                "id": msg.reply_to_message.from_user.id,
                "type": "user"
            }

        payload["messages"].append({
            "entities": [],
            "avatar": True,
            "from": {
                "id": msg.from_user.id,
                "name": msg.from_user.first_name or "NoName",
                "username": msg.from_user.username or "",
                "type": "user"
            },
            "text": msg.text or msg.caption or "",
            "reply": reply_data
        })

    async with aiohttp.ClientSession() as session:
        async with session.post(QUOTLY_API, json=payload) as resp:
            if resp.status != 200:
                raise Exception(f"API error {resp.status}")
            image_bytes = await resp.read()

    bio_sticker = BytesIO(image_bytes)
    bio_sticker.name = "quote.webp"
    return bio_sticker


@app.on_message(filters.command("qcolor"))
async def qcolor_handler(_, message: Message):
    warna_list = "\n• " + "\n• ".join(QUOTE_COLORS)
    await message.reply_text(f"<blockquote>🎨 **Daftar warna Quote:**{warna_list}</blockquote>")


@app.on_message(filters.command(["q", "qr"], prefixes=["/", "!", "."]))
async def quote_handler(client, message):
    print("✅ /q handler terpanggil:", message.text)  # Debug di console

    if not message.reply_to_message:
        return await message.reply_text("<blockquote>⚠️ Balas pesan yang ingin di-quote!</blockquote>")

    try:
        # Panggil API Quotly
        url = "https://bot.lyo.su/quote/generate"
        payload = {
            "messages": [
                {
                    "text": message.reply_to_message.text or "",
                    "from": {
                        "id": message.reply_to_message.from_user.id,
                        "name": message.reply_to_message.from_user.first_name
                    }
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    return await message.reply_text(f"<blockquote>⚠️ API gagal. Status: {resp.status}</blockquote>")

                data = await resp.json()
                img_url = data.get("result", {}).get("image")

                if not img_url:
                    return await message.reply_text("<blockquote>⚠️ API tidak mengembalikan gambar</blockquote>")

                await message.reply_photo(img_url)

    except Exception as e:
        print("❌ Error di /q:", e)
        await message.reply_text("<blockquote>⚠️ Terjadi kesalahan saat membuat quote</blockquote>")


__MODULES__ = "Quote"
__HELP__ = """<blockquote>Command Help **Quote**</blockquote>

<blockquote>**Make quote text with color** </blockquote>
    **You can make quote the message with random color or custom color just give name color after command**
        `{0}q pink` (reply message)

<blockquote>**Make fake quote text** </blockquote>
    **You can make fake quote user the message with this message**
        `{0}q @dreamskyzi` (reply message)

<blockquote>**Make reply-style quote** </blockquote>
    **Like real Telegram reply quote**
        `{0}qr` (reply message)

<blockquote>**View quote color** </blockquote>
    **Get supported color for quote**
        `{0}qcolor`

<b>   {1}</b>
"""