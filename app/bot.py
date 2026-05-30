import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Welcome to Spotify Playlist Assistant 🎵"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(
        CommandHandler("start", start)
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
