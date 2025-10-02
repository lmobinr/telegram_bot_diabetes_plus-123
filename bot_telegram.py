import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI

# گرفتن توکن‌ها از متغیر محیطی
TELEGRAM_TOKEN = ('8477905167:AAF7ZmAam7XumyFQOGqxz5_MKh-nCiTCAYc')
OPENAI_API_KEY = ("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")
WEBHOOK_URL = ("https://telegram-bot-diabetes-plus-123.onrender.com")  # مثلا: https://your-app.onrender.com/webhook

# اتصال به OpenAI
client = OpenAI(api_key='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')

# ساخت اپ Flask
app = Flask(__name__)
application = Application.builder().token('8477905167:AAF7ZmAam7XumyFQOGqxz5_MKh-nCiTCAYc').build()

# دستور /start
async def start(update: Update, context):
    await update.message.reply_text("من یه بات هوشمند هستم که به هوش مصنوعی وصلم از طرف مبین مددی تقدیم به لیدر پارام ")

# هندل پیام‌ها
async def chat(update: Update, context):
    user_message = update.message.text.strip()

    # فرستادن به ChatGPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",   # می‌تونی gpt-4 هم بذاری
        messages=[{"role": "user", "content": user_message}]
    )

    bot_reply = response.choices[0].message.content
    await update.message.reply_text(bot_reply)

# اضافه کردن هندلرها
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# اتصال Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # ست کردن وبهوک    
    application.bot.set_webhook(url='https://telegram-bot-diabetes-plus-123.onrender.com' + "/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


