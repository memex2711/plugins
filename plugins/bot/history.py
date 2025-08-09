import asyncio
import random
import time

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import Message

from ChampuMusic import app
from ChampuMusic.core.userbot import assistants
from ChampuMusic.utils.database import get_client

# Cache untuk menghindari spam
last_checked = {}

async def get_sangmata_history(user_id: int):
    """Ambil history dari sangmata_bot untuk user_id"""
    sgbot = ["SangMata_Bot", "SangMata_beta_bot"]
    sg = random.choice(sgbot)
    CHAMPU = random.choice(assistants)
    ubot = await get_client(CHAMPU)

    try:
        msg = await ubot.send_message(sg, str(user_id))
        await msg.delete()
    except Exception as e:
        return f"❌ Error: {e}"

    await asyncio.sleep(1)

    async for stalk in ubot.search_messages(sg):
        if stalk.text:
            # Hapus history chat dengan sangmata_bot
            try:
                user_info = await ubot.resolve_peer(sg)
                await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
            except:
                pass
            return stalk.text

    return None


@app.on_message(filters.command(["sg", "History"]))
async def manual_sg(client: Client, message: Message):
    """Perintah manual /sg"""
    if len(message.text.split()) < 2 and not message.reply_to_message:
        return await message.reply("<blockquote>⚠️ Balas pesan atau tulis ID/username.</blockquote>")

    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1:]
        if not args:
            return await message.reply("<blockquote>⚠️ Masukkan username/ID.</blockquote>")
        target_id = args[0]

    lol = await message.reply("<code>Processing...</code>")
    try:
        user = await client.get_users(str(target_id))
    except:
        return await lol.edit("<blockquote>⚠️ User tidak valid.</blockquote>")

    result = await get_sangmata_history(user.id)
    if not result:
        await lol.edit("<blockquote>⚠️ Tidak ada data dari SangMata.</blockquote>")
    else:
        await lol.edit(result)


@app.on_message(filters.group & ~filters.bot)
async def auto_sg(client: Client, message: Message):
    """Cek otomatis setiap kali ada user kirim pesan"""
    if not message.from_user:
        return

    user_id = message.from_user.id
    now = time.time()

    # Jangan cek kalau baru saja dicek (1 jam cooldown)
    if user_id in last_checked and now - last_checked[user_id] < 3600:
        return

    last_checked[user_id] = now

    result = await get_sangmata_history(user_id)
    if result:
        await message.reply_text(result)


__MODULE__ = "Hɪsᴛᴏʀʏ"
__HELP__ = """
<blockquote expandable>## Hɪsᴛᴏʀʏ Cᴏᴍᴍᴀɴᴅs Hᴇᴘ

### 1. /sɢ ᴏʀ /Hɪsᴛᴏʀʏ
**Dᴇsᴄʀɪᴘᴛɪᴏɴ:**
Fᴇᴛᴄʜᴇs ᴀ ʀᴀɴᴅᴏᴍ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ʜɪsᴛᴏʀʏ.

**Usᴀɢᴇ:**
/sɢ [ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ʀᴇᴘʏ]

**Dᴇᴛᴀɪs:**
- Fᴇᴛᴄʜᴇs ᴀ ʀᴀɴᴅᴏᴍ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴍᴇssᴀɢᴇ ʜɪsᴛᴏʀʏ ᴏғ ᴛʜᴇ sᴘᴇᴄɪғɪᴇᴅ ᴜsᴇʀ.
- Cᴀɴ ʙᴇ ᴜsᴇᴅ ʙʏ ᴘʀᴏᴠɪᴅɪɴɢ ᴀ ᴜsᴇʀɴᴀᴍᴇ, ᴜsᴇʀ ID, ᴏʀ ʀᴇᴘʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴜsᴇʀ.
- Aᴄᴄᴇssɪʙᴇ ᴏɴʏ ʙʏ ᴛʜᴇ ʙᴏᴛ's ᴀssɪsᴛᴀɴᴛs.

**Exᴀᴍᴘᴇs:**
- `/sɢ ᴜsᴇʀɴᴀᴍᴇ`
- `/sɢ ᴜsᴇʀ_ɪᴅ`
- `/sɢ [ʀᴇᴘʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]`</blockquote>
"""
