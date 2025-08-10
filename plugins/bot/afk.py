from datetime import datetime
from dateutil import parser
from pyrogram import filters
from ChampuMusic import app
from ChampuMusic.utils.database import set_afk, get_afk, remove_afk  # fungsi db

# Command /afk (bisa dipakai semua user)
@app.on_message(filters.command("afk"))
async def set_afk_cmd(_, message):
    reason = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "AFK"
    await set_afk(message.from_user.id, reason)
    await message.reply_text(f"gwej afk ☝️😹\n {reason}</blockquote>")

# BRB tanpa slash (contoh: brb tidur) (bisa dipakai semua user)
@app.on_message(filters.regex(r"(?i)^brb(?:\s+(.+))?$"))
async def set_brb_cmd(_, message):
    reason = message.matches[0].group(1) if message.matches[0].group(1) else "brb mulu lu pler"
    await set_afk(message.from_user.id, reason)
    await message.reply_text(
        f"<blockquote>gwej afk ☝️😹\n{reason}\n</blockquote>"
    )

# Auto balas jika ada yang mention / reply
@app.on_message(filters.group & (filters.mentioned | filters.reply))
async def mention_afk(_, message):
    if not message.from_user:
        return

    afk_user_id = None

    if message.reply_to_message and message.reply_to_message.from_user:
        afk_user_id = message.reply_to_message.from_user.id
    else:
        if message.entities:
            for ent in message.entities:
                if ent.type == "text_mention" and ent.user:
                    afk_user_id = ent.user.id
                    break
                elif ent.type == "mention":
                    username = message.text[ent.offset : ent.offset + ent.length]
                    username = username[1:]
                    try:
                        user = await app.get_users(username)
                        afk_user_id = user.id
                        break
                    except Exception:
                        continue

    if not afk_user_id:
        return

    data = await get_afk(afk_user_id)
    if data:
        start_time = data["start"]
        if isinstance(start_time, str):
            start_time = parser.parse(start_time)
        elapsed = datetime.utcnow() - start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        user = await app.get_users(afk_user_id)
        await message.reply_text(
            f"<blockquote><a href=\"tg://user?id={user.id}\">{user.first_name}</a> Afk! {hours}h {minutes}m\n{data['reason']}</blockquote>"
        )

# Hilangkan AFK kalau user kirim pesan
@app.on_message(filters.text)
async def remove_afk_handler(_, message):
    if not message.from_user:  # kalau bukan user (misal channel/system message)
        return

    data = await get_afk(message.from_user.id)
    if data:
        await remove_afk(message.from_user.id)
        await message.reply_text("<blockquote>udah online rek ☝️😹.</blockquote>")

__MODULE__ = "Bᴀɴ"
__HELP__ = """
/afk atau brb """