import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from keep_alive import keep_alive

# Завантаження токенів з .env файлу
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Змінна середовища для токена
YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID")  # Змінна середовища для вашого чату

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Welcome to the CodeCloud support service ✋ Here you can complain about a problem you encountered while visiting CodeCloud, or provide some idea of ​​your own for the performance of the web application, to do this, just send a photo/video to the chat 😁'
    )

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        '💨 Frequently asked questions:  Found an error? — Send a photo/video with a description of the problem.  How to contact the support service? — Write here or to the developer: @wtashame . Can I participate in CodeCloud development? — Contact the developer. 💨'
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    await update.message.reply_text('Thank you for your message! We will contact you as soon as possible!💖')
    await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"new message from {update.message.from_user.username}: {user_message}")

async def handle_photo(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive('received_photo.jpg')
        await update.message.reply_text('I see your photo. We will definitely review it👍')
        await context.bot.send_photo(chat_id=YOUR_CHAT_ID, photo=photo_file.file_id)

async def handle_video(update: Update, context: CallbackContext) -> None:
    if update.message.video:
        video_file = await update.message.video.get_file()
        await video_file.download_to_drive('received_video.mp4')
        await update.message.reply_text('I see your video. I am sending it to the support service✅')
        await context.bot.send_video(chat_id=YOUR_CHAT_ID, video=video_file.file_id)

def main():
    keep_alive()  # Підтримка активності сервера
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    application.run_polling()

if __name__ == '__main__':
    main()
