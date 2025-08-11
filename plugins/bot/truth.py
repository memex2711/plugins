import requests
from pyrogram import filters
from MoonMusic import app

truth_api_url = "https://api.truthordarebot.xyz/v1/truth"
dare_api_url = "https://api.truthordarebot.xyz/v1/dare"

@app.on_message(filters.command("truth"))
async def get_truth(client, message):
    try:
        response = requests.get(truth_api_url)
        if response.status_code == 200:
            truth_question = response.json()["question"]
            await message.reply_text(f"ᴛʀᴜᴛʜ ǫᴜᴇsᴛɪᴏɴ:\n\n{truth_question}")
        else:
            await message.reply_text(
                "ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴀ ᴛʀᴜᴛʜ ǫᴜᴇsᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
            )
    except Exception as e:
        await message.reply_text(
            "ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ғᴇᴛᴄʜɪɴɢ ᴀ ᴛʀᴜᴛʜ ǫᴜᴇsᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
        )

@app.on_message(filters.command("dare"))
async def get_dare(client, message):
    try:
        response = requests.get(dare_api_url)
        if response.status_code == 200:
            dare_question = response.json()["question"]
            await message.reply_text(f"ᴅᴀʀᴇ ǫᴜᴇsᴛɪᴏɴ:\n\n{dare_question}")
        else:
            await message.reply_text(
                "ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴀ ᴅᴀʀᴇ ǫᴜᴇsᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
            )
    except Exception as e:
        await message.reply_text(
            "ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ғᴇᴛᴄʜɪɴɢ ᴀ ᴅᴀʀᴇ ǫᴜᴇsᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
        )



__HELP__ = """
**ᴛʀᴜᴛʜ ᴏʀ ᴅᴀʀᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs**

ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴘʟᴀʏ ᴛʀᴜᴛʜ ᴏʀ ᴅᴀʀᴇ:

- `/truth`: ɢᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ᴛʀᴜᴛʜ ǫᴜᴇsᴛɪᴏɴ. ᴀɴsᴡᴇʀ ʜᴏɴᴇsᴛʟʏ!
- `/dare`: ɢᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ᴅᴀʀᴇ ᴄʜᴀʟʟᴇɴɢᴇ. ᴄᴏᴍᴘʟᴇᴛᴇ ɪᴛ ɪғ ʏᴏᴜ ᴅᴀʀᴇ!

**ᴇxᴀᴍᴘʟᴇs:**
- `/truth`: "ᴡʜᴀᴛ ɪs ʏᴏᴜʀ ᴍᴏsᴛ ᴇᴍʙᴀʀʀᴀssɪɴɢ ᴍᴏᴍᴇɴᴛ?"
- `/dare`: "ᴅᴏ 10 ᴘᴜsʜ-ᴜᴘs."

**ɴᴏᴛᴇ:**
ɪғ ʏᴏᴜ ᴇɴᴄᴏᴜɴᴛᴇʀ ᴀɴʏ ɪssᴜᴇs ᴡɪᴛʜ ғᴇᴛᴄʜɪɴɢ ǫᴜᴇsᴛɪᴏɴs, ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.
"""

__MODULE__ = "Tʀᴜᴛʜ"
