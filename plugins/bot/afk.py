from datetime import datetime
from pyrogram import filters
from ChampuMusic import app
from ChampuMusic.utils.database import set_afk, get_afk, remove_afk

# Command /afk
@app.on_message(filters.command("afk") & filters.me)
async def set_afk_cmd(_, message):
    reason = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "AFK"
    await set_afk(message.from_user.id, reason)
    await message.edit(f"✅ AFK diaktifkan\n**Alasan:** {reason}")

# BRB tanpa slash (contoh: brb tidur)
@app.on_message(filters.me & filters.regex(r"^(?i)brb\s+(.+)"))
async def set_brb_cmd(_, message):
    reason = message.matches[0].group(1)
    await set_afk(message.from_user.id, reason)
    await message.edit(f"✅ BRB diaktifkan\n**Alasan:** {reason}")

# Auto balas jika ada yang mention / reply
@app.on_message(filters.group & (filters.mentioned | filters.reply))
async def mention_afk(_, message):
    if not message.from_user:
        return

    afk_user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        afk_user_id = message.reply_to_message.from_user.id
    else:
        # cek mention entities jika ada
        if message.entities:
            for ent in message.entities:
                if ent.type == "mention" or ent.type == "text_mention":
                    # dapatkan id user dari mention
                    if ent.user:
                        afk_user_id = ent.user.id
                        break

    if not afk_user_id:
        return

    data = await get_afk(afk_user_id)
    if data:
        start_time = data["start"]
        elapsed = datetime.utcnow() - start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        user = await app.get_users(afk_user_id)
        await message.reply_text(
            f"{user.first_name} Afk! {hours}h {minutes}m\n{data['reason']}"
        )

# Hilangkan AFK kalau user kirim pesan
@app.on_message(filters.me & filters.text)
async def remove_afk(_, message):
    data = await get_afk(message.from_user.id)
    if data:
        await remove_afk(message.from_user.id)
        await message.reply_text("✅ Status AFK/BRB dihapus.")

__MODULE__ = "Bᴀɴ"
__HELP__ = """
/afk atau brb """