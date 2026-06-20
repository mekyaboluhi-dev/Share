from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string

API_ID = 31053465
API_HASH = "557478eb1546473d5d4da5a15990b379"
BOT_TOKEN = "8447170959:AAEs8F8EGsjh9yziyMoHnPggKKA1_1xPxSE"

STORAGE_CHANNEL = -1003616852310

bot = Client("filesharebot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_files = {}
file_groups = {}

START_MESSAGE = """
📂 Welcome to Advanced File Share Bot

You can upload and share files easily.

Choose an option below 👇
"""

MAIN_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📤 Upload File", callback_data="upload")],
    [InlineKeyboardButton("📢 Join Channel", url="https://t.me/Hackerinternetfile")],
    [InlineKeyboardButton("🔗 Get Share Link", callback_data="getlink")],
    [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
])


@bot.on_message(filters.command("start"))
async def start(client, message):

    if len(message.command) > 1:

        key = message.command[1]

        if key in file_groups:
            files = file_groups[key]

            for msg_id in files:
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=STORAGE_CHANNEL,
                    message_id=msg_id
                )
            return

    await message.reply(
        START_MESSAGE,
        reply_markup=MAIN_BUTTONS
    )


@bot.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def save_file(client, message):

    msg = await message.copy(STORAGE_CHANNEL)

    user_id = message.from_user.id

    if user_id not in user_files:
        user_files[user_id] = []

    user_files[user_id].append(msg.id)

    await message.reply("✅ File saved. Upload more or click Get Share Link.")


@bot.on_callback_query()
async def callback(client, query):

    user_id = query.from_user.id

    if query.data == "getlink":

        if user_id not in user_files or len(user_files[user_id]) == 0:
            await query.message.reply("❌ No files uploaded")
            return

        files = user_files[user_id]

        key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        file_groups[key] = files

        user_files[user_id] = []

        link = f"https://t.me/{(await bot.get_me()).username}?start={key}"

        await query.message.reply(
            f"🔗 Your Share Link\n\n{link}"
        )

    elif query.data == "upload":
        await query.message.reply("📤 Send any file to upload")

    elif query.data == "help":
        await query.message.reply(
"""
ℹ️ How to use this bot

1️⃣ Send any file
2️⃣ Upload multiple files
3️⃣ Click Get Share Link
4️⃣ Share link with friends
"""
        )

print("Bot Running...")

bot.run()