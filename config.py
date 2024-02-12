import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "")
    API_HASH  = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

    # database config
    DB_NAME = os.environ.get("DB_NAME","miku")     
    DB_URL  = os.environ.get("DB_URL","")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://te.legra.ph/file/f6faf6f76ccd1052b0499.mp4")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '5971676967').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Anime_Kun_Channel") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):

    SEQUENCE_TXT = """Sequence Bot will be added soon 😶‍🌫️.

    
    """
        
    START_TXT = """Hᴇʏ Tʜᴇʀᴇ {}!!
Oʀᴇ Nᴏ Nᴀᴡᴀ **Mɪᴋᴜ Nᴀᴋᴀɴᴏ**, ᴀ ꜰᴀsᴛ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ʙᴏᴛ ᴡʜᴏ's ɢᴏɴɴᴀ ᴍᴀᴋᴇ ʏᴏᴜʀ ꜰɪʟᴇs/ᴠɪᴅᴇᴏ ʀᴇɴᴀᴍɪɴɢ ᴘʀᴏᴄᴇss ʀᴇᴀʟ qᴜɪᴄᴋ ᴀɴᴅ ᴇᴀsʏ.

ᴛᴏ ᴋɴᴏᴡ ᴡʜᴀᴛ I'ᴍ ᴄᴀᴘᴀʙʟᴇ ᴏꜰ ᴏᴛʜᴇʀ ᴛʜᴀɴ ᴍᴀss-ᴍᴀssᴀᴄʀᴇ, ʙᴇᴛᴛᴇʀ ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ.. 🕊️"""
    
    FILE_NAME_TXT = """
    <u><b>SETUP AUTO RENAME FORMAT</b></u>\n\nUse These Keywords To Setup Custom File Name\n\n➝ episode :- to replace episode number\n➝ quality :- to replace video resolution\n\n‣ <b>Example :</b> /autorename [CW] Attack on Titan S1 - episode [quality] [Dual] @Anime_Kun_Channel\n\n‣ <b>Your Current Rename Format :</b> {format_template}
    """
    
    ABOUT_TXT = f"""<b>╭───────────⍟
├🦥 Owner: <a href=http://t.me/Chowdhury_Siam>Sɪᴀᴍ Cʜᴏᴡᴅʜᴜʀʏ</a>
├📕 Library: <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
├✏️ Language: <a href=https://www.python.org>Pyᴛʜᴏɴ3</a>
├💾 Data Base: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
├📊 Build Version: `Mɪᴋᴜ V1.7.0`
╰───────────────⍟ 
"""

    
    THUMB_TXT = """ • /start the bot and send any photo to automatically set the thumbnail.
• /del_thumb to delete your old thumbnail.
• /view_thumb to view your current thumbnail."""

    PREMIUM_TXT = """Not Decided Yet"""

    COMMANDS_TXT = """🌌 How To Set Thumbnail
  
• /start the bot and send any photo to automatically set the thumbnail.
• /del_thumb to delete your old thumbnail.
• /view_thumb to view your current thumbnail.

📑 How To Set Custom Caption
• /set_caption - Use this command to set a custom caption.
• /see_caption - Use this command to view your custom caption.
• /del_caption - Use this command to delete your custom caption.
Example: /set_caption 📕 File Name: {filename}
💾 Size: {filesize}
⏰ Duration: {duration}

✏️ How To Rename A File
• First set /autorename format then send your files. Eg: /autorename [S01-episode] Attack on Titan [quality] [Dual] @Anime_Kun_Channel

‣ Available Variables
» <code>episode</code>
» <code>quality</code>

• Default Format Type Set to [document].mkv    """

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""


