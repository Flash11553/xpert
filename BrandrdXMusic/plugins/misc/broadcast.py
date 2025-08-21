import asyncio
import logging
from typing import Iterable, List, Tuple

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import (
    FloodWait,
    RPCError,
    PeerIdInvalid,
    UserIsBlocked,
    UserDeactivated,
    ChatAdminRequired,
    ChannelPrivate,
    ChatWriteForbidden,
)

from BrandrdXMusic import app
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from BrandrdXMusic.utils.decorators.language import language
from BrandrdXMusic.utils.formatters import alpha_to_int
from config import adminlist

# Optional cleanup helpers
try:
    from BrandrdXMusic.utils.database import del_served_chat  # type: ignore
except Exception:
    del_served_chat = None  # type: ignore

try:
    from BrandrdXMusic.utils.database import del_served_user  # type: ignore
except Exception:
    del_served_user = None  # type: ignore


IS_BROADCASTING = False

# --- Configurable ---
BATCH_SIZE_CHATS = 50
BATCH_SIZE_USERS = 100
DELAY_BETWEEN_MESSAGES = 0.5
DELAY_BETWEEN_BATCHES = 5.0
ASSISTANT_DELAY = 3.0
MAX_FLOODWAIT_TO_SKIP = None  # None = never skip


# -------- utils --------
def chunked(seq: List[int], n: int) -> Iterable[List[int]]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _parse_flags_from_query(raw: str) -> Tuple[str, dict]:
    flags = {
        "pin": False,
        "pinloud": False,
        "assistant": False,
        "user": False,
        "nobot": False,
    }
    if "-pinloud" in raw:
        flags["pinloud"] = True
        raw = raw.replace("-pinloud", "")
    if "-pin" in raw:
        flags["pin"] = True
        raw = raw.replace("-pin", "")
    if "-assistant" in raw:
        flags["assistant"] = True
        raw = raw.replace("-assistant", "")
    if "-user" in raw:
        flags["user"] = True
        raw = raw.replace("-user", "")
    if "-nobot" in raw:
        flags["nobot"] = True
        raw = raw.replace("-nobot", "")
    return raw.strip(), flags


async def _safe_pin(m, loud: bool) -> bool:
    try:
        await m.pin(disable_notification=not loud)
        return True
    except Exception as e:
        logging.debug(f"Pin failed: {e}")
        return False


async def _handle_floodwait(fw: FloodWait) -> None:
    sleep_for = int(getattr(fw, "value", getattr(fw, "x", 1)))
    if MAX_FLOODWAIT_TO_SKIP is not None and sleep_for > MAX_FLOODWAIT_TO_SKIP:
        raise fw
    logging.warning(f"FloodWait: sleeping for {sleep_for}s")
    await asyncio.sleep(sleep_for)


def _is_terminal_delivery_error(e: Exception) -> bool:
    return isinstance(
        e,
        (
            PeerIdInvalid,
            UserIsBlocked,
            UserDeactivated,
            ChannelPrivate,
            ChatWriteForbidden,
        ),
    )


async def _maybe_cleanup_chat(chat_id: int) -> None:
    if del_served_chat:
        try:
            await del_served_chat(chat_id)
        except Exception as e:
            logging.debug(f"Failed to remove chat {chat_id}: {e}")


async def _maybe_cleanup_user(user_id: int) -> None:
    if del_served_user:
        try:
            await del_served_user(user_id)
        except Exception as e:
            logging.debug(f"Failed to remove user {user_id}: {e}")


# --------- main command ---------
@app.on_message(filters.command("broadcast") & SUDOERS)
@language
async def broadcast_message(client, message, _):
    global IS_BROADCASTING

    if message.reply_to_message:
        source_msg_id = message.reply_to_message.id
        source_chat_id = message.chat.id
        query_text = None
        flags = {
            "pin": False,
            "pinloud": False,
            "assistant": False,
            "user": False,
            "nobot": False,
        }
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        raw_query = message.text.split(None, 1)[1]
        query_text, flags = _parse_flags_from_query(raw_query)
        if not query_text:
            return await message.reply_text(_["broad_8"])
        source_msg_id = None
        source_chat_id = None

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    total_sent_chats = 0
    total_pinned = 0
    failed_chats: List[int] = []

    total_sent_users = 0
    failed_users: List[int] = []

    # --- Broadcast to chats ---
    if not flags.get("nobot", False):
        served = await get_served_chats()
        chat_ids = [int(c["chat_id"]) for c in served]

        for batch in chunked(chat_ids, BATCH_SIZE_CHATS):
            for chat_id in batch:
                try:
                    if source_msg_id is not None:
                        m = await app.forward_messages(chat_id, source_chat_id, source_msg_id)
                    else:
                        m = await app.send_message(chat_id, text=query_text)

                    if flags.get("pin"):
                        if await _safe_pin(m, loud=False):
                            total_pinned += 1
                    elif flags.get("pinloud"):
                        if await _safe_pin(m, loud=True):
                            total_pinned += 1

                    total_sent_chats += 1
                    await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
                except FloodWait as fw:
                    try:
                        await _handle_floodwait(fw)
                        if source_msg_id is not None:
                            m = await app.forward_messages(chat_id, source_chat_id, source_msg_id)
                        else:
                            m = await app.send_message(chat_id, text=query_text)
                        total_sent_chats += 1
                    except Exception as e:
                        logging.warning(f"Skipping chat {chat_id}: {e}")
                        failed_chats.append(chat_id)
                        if _is_terminal_delivery_error(e):
                            await _maybe_cleanup_chat(chat_id)
                except (ChatAdminRequired, RPCError) as e:
                    failed_chats.append(chat_id)
                    if _is_terminal_delivery_error(e):
                        await _maybe_cleanup_chat(chat_id)
                except Exception as e:
                    failed_chats.append(chat_id)
            await asyncio.sleep(DELAY_BETWEEN_BATCHES)

        try:
            await message.reply_text(_["broad_3"].format(total_sent_chats, total_pinned))
        except Exception:
            pass

    # --- Broadcast to users ---
    if flags.get("user", False):
        served_u = await get_served_users()
        user_ids = [int(u["user_id"]) for u in served_u]

        for batch in chunked(user_ids, BATCH_SIZE_USERS):
            for user_id in batch:
                try:
                    if source_msg_id is not None:
                        await app.forward_messages(user_id, source_chat_id, source_msg_id)
                    else:
                        await app.send_message(user_id, text=query_text)
                    total_sent_users += 1
                    await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
                except FloodWait as fw:
                    try:
                        await _handle_floodwait(fw)
                        if source_msg_id is not None:
                            await app.forward_messages(user_id, source_chat_id, source_msg_id)
                        else:
                            await app.send_message(user_id, text=query_text)
                        total_sent_users += 1
                    except Exception as e:
                        failed_users.append(user_id)
                        if _is_terminal_delivery_error(e):
                            await _maybe_cleanup_user(user_id)
                except RPCError as e:
                    failed_users.append(user_id)
                    if _is_terminal_delivery_error(e):
                        await _maybe_cleanup_user(user_id)
                except Exception as e:
                    failed_users.append(user_id)
            await asyncio.sleep(DELAY_BETWEEN_BATCHES)

        try:
            await message.reply_text(_["broad_4"].format(total_sent_users))
        except Exception:
            pass

    # --- Assistants ---
    if flags.get("assistant", False):
        status_msg = await message.reply_text(_["broad_5"])
        text_accum = _["broad_6"]
        from AnonXMusic.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    if source_msg_id is not None:
                        await client.forward_messages(dialog.chat.id, source_chat_id, source_msg_id)
                    else:
                        await client.send_message(dialog.chat.id, text=query_text or _["broad_6"])
                    sent += 1
                    await asyncio.sleep(ASSISTANT_DELAY)
                except Exception as e:
                    logging.debug(f"Assistant {num} skip: {e}")
                    continue
            text_accum += _["broad_7"].format(num, sent)
        try:
            await status_msg.edit_text(text_accum)
        except Exception:
            pass

    IS_BROADCASTING = False


# --- Background auto-clean ---
async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges and user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except Exception as e:
            logging.debug(f"auto_clean error: {e}")
            continue


asyncio.create_task(auto_clean())
