import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

def init_db():
    conn = sqlite3.connect("members.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            telegram_id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Share My Number", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "👋 Welcome to the VIP Betting Community!\n\nTap the button below to get SMS alerts for our picks 👇",
        reply_markup=keyboard
    )

async def contact_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    name = update.effective_user.first_name
    phone = contact.phone_number
    telegram_id = update.effective_user.id

    conn = sqlite3.connect("members.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO members (telegram_id, name, phone)
        VALUES (?, ?, ?)
    """, (telegram_id, name, phone))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Done {name}! You'll now receive our picks via SMS 🔥")

init_db()
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, contact_received))
app.run_polling()
