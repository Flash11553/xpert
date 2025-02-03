import requests
from BrandrdXMusic import app
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

@app.on_message(filters.command(["chatgpt", "ai", "ask", "gpt", "effect"], prefixes=[".", "!", "/", ""]))
async def chat_gpt(bot, message):
    try:
        # Indicate typing action
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        # Get the user's name or set a default value
        name = message.from_user.first_name if message.from_user else "User"

        # Check if a query was provided
        if len(message.command) < 2:
            await message.reply_text(f"**Salam {name} Effect eşidir, Sizə necə kömək edə bilərəm?**")
        else:
            query = message.text.split(' ', 1)[1]  # Extract query text
            api_url = f"https://darkness.ashlynn.workers.dev/chat/?prompt={query}"

            # Make API request
            response = requests.get(api_url).json()

            # Extract and send the response if successful
            if response.get("successful") == "success":
                bot_response = response.get("response", "No response provided.")
                await message.reply_text(f"{bot_response}", parse_mode=ParseMode.MARKDOWN)
            else:
                await message.reply_text("**Failed to fetch a response. Please try again later.**")
    except Exception as e:
        await message.reply_text(f"**Error: {e}**")
