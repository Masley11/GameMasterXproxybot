from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio

app = Flask(__name__)

# Remplacez 'YOUR_TOKEN' par le token de votre bot
TELEGRAM_TOKEN = 'YOUR_TOKEN'

# Créez une instance de l'Application
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Chemin vers le fichier à télécharger
FILE_PATH = 'path/to/your/file.ext'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Traitez la mise à jour reçue de Telegram
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return 'ok'

# Définissez la commande /start
async def start(update: Update, context):
    await update.message.reply_text('Bienvenue! Envoyez-moi un lien pour obtenir votre fichier.')

# Gérez les messages texte
async def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    with open(FILE_PATH, 'rb') as file:
        await context.bot.send_document(chat_id=chat_id, document=file)

# Ajoutez les handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    # Démarrez le serveur Flask
    app.run(port=5000)
