from datetime import datetime
from pyrogram import filters
from ChampuMusic import app

# Penyimpanan status AFK
AFK_STATUS = {}  # { user_id: { "reason": str, "start": datetime } }

# Command /afk
@app.on_message(filters.command("afk") & filters.me)
async def set_afk(_, message):
    reason = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "AFK"
    AFK_STATUS[message.from_user.id] = {
        "reason": reason,
        "start": datetime.now()
    }
    await message.edit(f"✅ AFK diaktifkan\n**Alasan:** {reason}")

# BRB tanpa slash (contoh: brb tidur)
@app.on_message(filters.me & filters.regex(r"^(?i)brb\s+(.+)"))
async def set_brb(_, message):
    reason = message.matches[0].group(1)
    AFK_STATUS[message.from_user.id] = {
        "reason": reason,
        "start": datetime.now()
    }
    await message.edit(f"✅ BRB diaktifkan\n**Alasan:** {reason}")

# Auto balas jika ada yang mention / reply
@app.on_message(filters.group & (filters.mentioned | filters.reply))
async def mention_afk(_, message):
    if not message.from_user:
        return
    for afk_user_id, data in AFK_STATUS.items():
        # Cek apakah yang ditag user AFK
        if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == afk_user_id:
            await send_afk_info(message, afk_user_id, data)
        elif message.entities:
            if any(ent.type == "mention" and f"@{message.reply_to_message.from_user.username}" for ent in message.entities):
                await send_afk_info(message, afk_user_id, data)

# Hilangkan AFK kalau user kirim pesan
@app.on_message(filters.me & filters.text)
async def remove_afk(_, message):
    if message.from_user.id in AFK_STATUS:
        AFK_STATUS.pop(message.from_user.id)
        await message.reply_text("✅ Status AFK/BRB dihapus.")

# Fungsi kirim info AFK
async def send_afk_info(message, user_id, data):
    start_time = data["start"]
    elapsed = datetime.now() - start_time
    hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    user = await app.get_users(user_id)
    await message.reply_text(
        f"{user.first_name} Afk! {hours}h {minutes}m\n{data['reason']}"
    )