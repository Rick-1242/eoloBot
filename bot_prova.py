from telegram.ext import *
from telegram import *
from requests import *

with open("token.txt", "r") as f:
    TOKEN = f.read()
    print("Il tuo token è: ", TOKEN)

isEnergyClicked = False
Mappa = "Mappa"
Energia = "Energia"

def start(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Mappa")], [(KeyboardButton("Energia"))]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Benvenuto nel bot", 
    reply_markup=ReplyKeyboardMarkup(buttons))


def help (update, context):
    update.message.reply_text("""
            Sono disponibili i seguenti comandi
    
            /start --> Messaggio di benevuto
            /help --> Questo messaggio
            /content --> Informazioni riguardo al corso
            /contact --> I miei contatti

    """)
def content (update, context):
    update.message.reply_text("Il nostro contenuto")

def contact (update, context):
    update.message.reply_text("I miei contatti")

def handle_message(update: Update, context: CallbackContext):
    global isEnergyClicked
    if isEnergyClicked:
        position(update, context)
        isEnergyClicked = False
    else:
        if Mappa in update.message.text:
            #image = get(immagine della mappa?).content
            update.message.reply_text("1. Coming soon")
        elif Energia in update.message.text:
            isEnergyClicked = True
            update.message.reply_text("Con questo comando puoi calcolare l'energia che avrebbe prodotto un'elica. Inserire un indirizzo.")
        else:
            update.message.reply_text("Comando non valido")


def ind(update, context):
    update.message.reply_text("Ben fatto buddy hai superato la prima prova.")
    buttons = [[KeyboardButton("Valori cristiani")], [(KeyboardButton("CSGO"))]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ora scegli attentamente", 
    reply_markup=ReplyKeyboardMarkup(buttons))

def position (update, context):
        indirizzo = update.message.text
        update.message.reply_text(indirizzo)
        ind(update, context)
    
def co(update, context):
    if isEnergyClicked == True:
        update.message.reply_text("True")
    else:
        update.message.reply_text("False")

updater = Updater(TOKEN, use_context = True)
disp = updater.dispatcher

disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("help", help))
disp.add_handler(CommandHandler("content", content))
disp.add_handler(CommandHandler("contact", contact))
disp.add_handler(CommandHandler("true", co))
disp.add_handler(MessageHandler(Filters.text, handle_message))

    
updater.start_polling()
updater.idle()

        
