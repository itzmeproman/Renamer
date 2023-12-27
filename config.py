import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "22418774")
    API_HASH  = os.environ.get("API_HASH", "d8c8dab274f9a811814a6a96d044028e")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6451712184:AAGa_lWsF2-Hnt1KZxPJb0RD2dsBDNDcWy0") 

    # database config
    DB_NAME = os.environ.get("DB_NAME","obi")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://mehtadmphta33:Mehtab1234@cluster0.bfsb3oq.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://graph.org/file/a39c43ccf6c454d30eaec.mp4")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6265459491 6299128233').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "UchihaPoliceUpdates") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002008965715"))

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):
    # part of text configuration
        
    START_TXT = """Hello {}
I'm **Obito Uchiha**, an autorename bot that renames anime files to the format you set."
To see my functions, use the buttons below."""
    
    FILE_NAME_TXT = """
    <u><b>SETUP AUTO RENAME FORMAT</b></u>\n\nUse These Keywords To Setup Custom File Name\n\n➝ episode :- to replace episode number\n➝ quality :- to replace video resolution\n\n‣ <b>Example :</b> /autorename [AL] High Card S1 - Eepisode [quality] Sub @Anime_Locus.mkv\n\n‣ <b>Your Current Rename Format :</b> {format_template}
    """
    
    ABOUT_TXT = f"""
Idk credit kisko du avi..
"""

    
    THUMB_TXT = """ just send the image."""

    PREMIUM_TXT = """Hm Soon
    for now free use kr lo"""

#⚠️ Dᴏɴ'ᴛ Rᴇᴍᴏᴠᴇ Oᴜʀ Cʀᴇᴅɪᴛꜱ @ᴩyʀᴏ_ʙᴏᴛᴢ🙏🥲
    COMMANDS_TXT = """<b><u>/autorename - user format</b></u>
    """

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""


