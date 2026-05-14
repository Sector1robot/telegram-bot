import os
import json
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
SHEET_ID = os.environ.get("SHEET_ID")
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")

IMAGE_URL = "https://i.ibb.co/twgTsdxf/Chat-GPT-Image-13-svi-2026-20-55-23.png"
EBOOK_URL = "https://drive.google.com/file/d/1maKFzB6reluizGpZ8tHZ4tac6pm1PWZs/view?usp=drive_link"

MESSAGES = {
    "Balkan": {
        "image": "https://i.ibb.co/1GRf0Q8F/Chat-GPT-Image-13-svi-2026-22-40-58.png",
        "welcome": "*🇭🇷🇧🇦🇷🇸🇲🇪🇸🇮 Odlično!*\n\nDa bi primio *World Cup Ebook* sa svim važnim stvarima i predikcijama, klikni ispod i poslat ćemo ga direktno na tvoj broj mobitela 👇",
        "success": "✅ *Savršeno! Registracija uspješna!* Pripremi se za World Cup tipove! 🏆🔥\n\nKlikni ispod da preuzmete besplatni Ebook 👇",
        "wrong": "Ovo je automatska poruka, molimo klikni gore da odabereš i odgovoriš ☝",
    },
    "Sweden": {
        "image": "https://i.ibb.co/R49n42PG/Chat-GPT-Image-13-svi-2026-21-43-42.png",
        "welcome": "*🇸🇪 Välkommen!*\n\nFör att få *World Cup Ebook* med all viktig information och förutsägelser, klicka nedan så skickar vi det direkt till ditt telefonnummer 👇",
        "success": "✅ *Perfekt! Registreringen lyckades!* Gör dig redo för World Cup picks! 🏆🔥\n\nKlicka nedan för att ladda ner din gratis Ebook 👇",
        "wrong": "Detta är ett automatiskt meddelande, klicka ovan för att välja och svara ☝",
    },
    "Finland": {
        "image": "https://i.ibb.co/JRTCyM5n/Chat-GPT-Image-13-svi-2026-21-48-44.png",
        "welcome": "*🇫🇮 Tervetuloa!*\n\nSaadaksesi *World Cup Ebook* -kirjan, jossa on kaikki tärkeät tiedot ja ennusteet, klikkaa alla ja lähetämme sen suoraan puhelinnumeroosi 👇",
        "success": "✅ *Täydellinen! Rekisteröinti onnistui!* Valmistaudu World Cup vinkkeihin! 🏆🔥\n\nLataa ilmainen Ebook alla olevasta painikkeesta 👇",
        "wrong": "Tämä on automaattinen viesti, klikkaa yllä valitaksesi ja vastataksesi ☝",
    },
    "Norway": {
        "image": "https://i.ibb.co/rGDJzG5x/Chat-GPT-Image-13-svi-2026-21-27-00.png",
        "welcome": "*🇳🇴 Velkommen!*\n\nFor å motta *World Cup Ebook* med all viktig informasjon og spådommer, klikk nedenfor så sender vi det direkte til telefonnummeret ditt 👇",
        "success": "✅ *Perfekt! Registreringen var vellykket!* Gjør deg klar for World Cup-tips! 🏆🔥\n\nKlikk nedenfor for å laste ned din gratis Ebook 👇",
        "wrong": "Dette er en automatisk melding, vennligst klikk ovenfor for å velge og svare ☝",
    },
    "Netherlands": {
        "image": "https://i.ibb.co/279T0mcN/Chat-GPT-Image-13-svi-2026-21-35-52.png",
        "welcome": "*🇳🇱 Welkom!*\n\nOm het *World Cup Ebook* te ontvangen met alle belangrijke informatie en voorspellingen, klik hieronder en we sturen het direct naar je telefoonnummer 👇",
        "success": "✅ *Perfect! Registratie geslaagd!* Maak je klaar voor World Cup tips! 🏆🔥\n\nKlik hieronder om je gratis Ebook te downloaden 👇",
        "wrong": "Dit is een automatisch bericht, klik hierboven om te selecteren en te antwoorden ☝",
    },
    "France": {
        "image": "https://i.ibb.co/Z1vLJ6Qs/Chat-GPT-Image-13-svi-2026-21-38-56.png",
        "welcome": "*🇫🇷 Bienvenue!*\n\nPour recevoir le *World Cup Ebook* avec toutes les informations importantes et les prédictions, cliquez ci-dessous et nous vous l'enverrons directement sur votre numéro de téléphone 👇",
        "success": "✅ *Parfait! Inscription réussie!* Préparez-vous pour les picks de la Coupe du Monde! 🏆🔥\n\nCliquez ci-dessous pour télécharger votre Ebook gratuit 👇",
        "wrong": "Ceci est un message automatique, veuillez cliquer ci-dessus pour sélectionner et répondre ☝",
    },
    "Bulgaria": {
        "image": "https://i.ibb.co/S7HMvT0v/Chat-GPT-Image-13-svi-2026-21-52-43.png",
        "welcome": "*🇧🇬 Добре дошли!*\n\nЗа да получиш *World Cup Ebook* с всички важни неща и прогнози, кликни по-долу и ще го изпратим директно на телефонния ти номер 👇",
        "success": "✅ *Перфектно! Регистрацията е успешна!* Пригответе се за прогнози от Световното! 🏆🔥\n\nКликнете по-долу, за да изтеглите безплатния Ebook 👇",
        "wrong": "Това е автоматично съобщение, моля кликнете по-горе, за да изберете и отговорите ☝",
    },
    "Other": {
        "image": "https://i.ibb.co/gZP0135N/Chat-GPT-Image-13-svi-2026-22-26-29.png",
        "welcome": "*🌍 Welcome!*\n\nTo receive the *World Cup Ebook* with all important stuff and predictions click below and we will send it directly to your phone number 👇",
        "success": "✅ *Perfect! Registration successful!* Get ready for World Cup picks! 🏆🔥\n\nClick below to download your free Ebook 👇",
        "wrong": "This is an automated message, please click above to select and answer ☝",
    },
}

COUNTRIES = [
    ("🇭🇷🇧🇦🇷🇸🇲🇪🇸🇮 Balkan", "Balkan"),
    ("🇸🇪 Sweden", "Sweden"),
    ("🇫🇮 Finland", "Finland"),
    ("🇳🇴 Norway", "Norway"),
    ("🇳🇱 Netherlands", "Netherlands"),
    ("🇫🇷 France", "France"),
    ("🇧🇬 Bulgaria", "Bulgaria"),
    ("🌍 Something else", "Other"),
]

def get_sheet():
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=code)]
        for label, code in COUNTRIES
    ])
    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption="*Sector1 World Cup Event IS HERE!!!* 🌍🏆\n\nWe prepared an Ebook for you to help you understand how Sector1 team is going to approach the BIGGEST EVENT on the market 🎯\n\nWe will also give you information on best picks and hot topic during the World Cup 🔥\n\nSelect where are you from 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def country_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data
    context.user_data["country"] = country

    msg = MESSAGES[country]
    button = KeyboardButton("📱 Share My Number", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await query.message.reply_photo(
        photo=msg["image"],
        caption=msg["welcome"],
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def contact_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    name = update.effective_user.first_name
    phone = contact.phone_number
    telegram_id = update.effective_user.id
    country = context.user_data.get("country", "Unknown")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    sheet = get_sheet()
    existing_ids = sheet.col_values(3)

    msg = MESSAGES.get(country, MESSAGES["Other"])
    download_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Download Free Ebook", url=EBOOK_URL)]
    ])

    if str(telegram_id) in existing_ids:
        await update.message.reply_text(
            msg["success"],
            reply_markup=download_button,
            parse_mode="Markdown"
        )
        return

    sheet.append_row([name, phone, str(telegram_id), country, date])

    await update.message.reply_text(
        msg["success"],
        reply_markup=download_button,
        parse_mode="Markdown"
    )

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = context.user_data.get("country", None)
    if country:
        reply = MESSAGES.get(country, MESSAGES["Other"])["wrong"]
    else:
        reply = "This is an automated message, please click above to select and answer ☝"
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(country_selected))
app.add_handler(MessageHandler(filters.CONTACT, contact_received))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))
app.run_polling()
