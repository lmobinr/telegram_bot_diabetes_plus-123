import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI

# ====== توکن‌ها ======
TELEGRAM_TOKEN = os.getenv("8477905167:AAF7ZmAam7XumyFQOGqxz5_MKh-nCiTCAYc") or "8477905167:AAF7ZmAam7XumyFQOGqxz5_MKh-nCiTCAYc"
OPENAI_API_KEY = os.getenv("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") or "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"
WEBHOOK_URL = os.getenv("https://telegram-bot-diabetes-plus-123.onrender.com/webhook") or "https://telegram-bot-diabetes-plus-123.onrender.com/webhook"

# ====== اتصال به OpenAI ======
client = OpenAI(api_key=OPENAI_API_KEY)

# ====== ساخت بات ======
application = Application.builder().token(TELEGRAM_TOKEN).build()

# ====== دستور /start ======
async def start(update: Update, context):
    await update.message.reply_text(
        "سلام! من یه بات هوشمند هستم که به هوش مصنوعی وصلم."
    )

# ====== هندل پیام‌ها ======
async def chat(update: Update, context):
    user_message = update.message.text.strip()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # یا gpt-4
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = "متاسفم، مشکلی پیش اومد! دوباره تلاش کن."
        print("OpenAI error:", e)
    
    await update.message.reply_text(bot_reply)

# ====== اضافه کردن هندلرها ======
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# ====== اجرای Webhook ======
if __name__ == "__main__":
    print("Bot is running...")
    asyncio.run(application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path="/webhook",
        webhook_url=WEBHOOK_URL
    ))
