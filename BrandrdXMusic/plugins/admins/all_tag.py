import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions
from BrandrdXMusic import app
from BrandrdXMusic.utils.branded_ban import admin_filter


SPAM_CHATS = []


@app.on_message(
    filters.command(["all", "mention", "mentionall", "utag", "tag"], prefixes=["/", "@", "#"])
    & admin_filter
)
async def tag_all_users(_, message):

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text(
            "** ᴛᴀɢ ᴘʀᴏsᴇsɪɴ ʙᴀşʟᴀᴛᴍᴀǫ üçüɴ ʙɪʀ söᴢ ʏᴀᴢıɴ ᴢəʜᴍəᴛ ᴏʟᴍᴀsᴀ,ʙᴜɴᴜɴ ᴋɪᴍɪ »** `@all Salam`"
        )
        return
    if replied:
        SPAM_CHATS.append(message.chat.id)
        usernum = 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"\n⊚ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 5:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]

        SPAM_CHATS.append(message.chat.id)
        usernum = 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"\n⊚ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 5:
                await app.send_message(
                    message.chat.id,
                    f"{text}\n{usertxt}\n\n|| ➥ ᴛᴀɢ ᴅᴀʏᴀɴᴅıʀᴍᴀǫ üçüɴ » /cancel ||",
                )
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass


@app.on_message(
    filters.command(
        [
            "stopmention",
            "offall",
            "cancel",
            "allstop",
            "stopall",
            "cancelmention",
            "offmention",
            "mentionoff",
            "alloff",
            "cancelall",
            "allcancel",
        ],
        prefixes=["/", "@", "#"],
    )
    & admin_filter
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass
        return await message.reply_text("𝗧𝗔𝗚 𝗘𝗧𝗠𝗘 𝗣𝗥𝗢𝗦𝗘𝗦𝗜 𝗗𝗔𝗬𝗔𝗡𝗗𝗜𝗥𝗜𝗟𝗗𝗜")

    else:
        await message.reply_text("**Hal hazırda tag prosesin başladan yoxdur**")
        return
