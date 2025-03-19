import random
import io
import requests
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient, events

# Define necessary values like bot name, username, and owner ID
BOT_NAME = "Effect"
BOT_USERNAME = "YourBotUsernamsje"
OWNER_ID = 5967971901  # Replace with your owner ID

LOGO_LINKS = [
    "https://telegra.ph/file/d1838efdafce9fe611d0c.jpg",
    "https://telegra.ph/file/c1ff2d5ec5e1b5bd1b200.jpg",
    "https://telegra.ph/file/08c5fbe14cc4b13d1de05.jpg",
    "https://telegra.ph/file/66614a049d74fe2a220dc.jpg",
    "https://telegra.ph/file/9cc1e4b24bfa13873bd66.jpg",
    # Add more URLs here as needed...
]

async def lego(event):
    # Get the query from the message
    quew = event.pattern_match.group(1)
    
    # Check if the sender is the owner or the query is provided
    if event.sender_id != OWNER_ID and not quew:
        await event.reply("You are not authorized to use this bot.")
        return
    
    # If a query is provided, handle the query
    if quew:
        # Pick a random logo from the list
        logo_url = random.choice(LOGO_LINKS)
        
        # Fetch the image
        response = requests.get(logo_url)
        logo_image = Image.open(io.BytesIO(response.content))

        # You can perform any image processing here
        # Example: Add text to the image
        draw = ImageDraw.Draw(logo_image)
        font = ImageFont.load_default()  # Use default font or load your own
        
        # Customize the text and position
        text = f"{BOT_NAME} - {quew}"
        text_position = (10, 10)  # Position of text (top-left corner)
        draw.text(text_position, text, fill="white", font=font)
        
        # Save the final image if needed
        output = io.BytesIO()
        logo_image.save(output, format="JPEG")
        output.seek(0)
        
        # Send the image back
        await event.reply(file=output)
    else:
        # If no query is provided, send a random logo
        logo_url = random.choice(LOGO_LINKS)
        
        # Fetch and send the logo image
        response = requests.get(logo_url)
        output = io.BytesIO(response.content)
        await event.reply(file=output)

# Run the bot
telethn.start()
telethn.run_until_disconnected()
