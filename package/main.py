import config
import sqlite3
import math as m
from telegram.ext import *
from geopy.geocoders import Nominatim


def get_loc(street: str) -> str:
    geolocator = Nominatim(user_agent="TelegramWindBot")
    location = geolocator.geocode(street)
    return location.longitude, location.latitude


def cloasest(update, context):  # TODO Make the bot take the adress as INPUT, find the coasest thing
    street = "Via Salvo d'acquisto,1 37122 Verona"
    print(context.args)
    coords = get_loc(street)
    update.message.reply_text(f"{coords[0]}, {coords[1]}")


def dist(lat1, lon1, lat2, lon2) -> float:
    """Calcutaes the distance between two coords

    Args:
        lat1 (float): latitude of first pos
        lon1 (float): longitude of first pos
        lat2 (float): latitude of second pos
        lon2 (float): longitude of second pos

    Returns:
        float: Distace in ?
    """
    num1 = m.sin((m.radians(lat2) - m.radians(lat1)) / 2)
    num2 = m.sin((m.radians(lon2) - m.radians(lon1)) / 2)
    return 6371 * 2 * m.asin(m.sqrt(m.pow(num1, 2) + m.cos(lat1) * m.cos(lat2) * m.pow(num2, 2)))


def start(update, context):
    """First msg the bot sends
    """
    update.message.reply_text("Ciao! Benvenuto nel bot prova /help")


def help(update, context):
    update.message.reply_text("""
    Sono disponibili i seguenti comandi:

    /start --> Messaggio di benvenuto
    /help --> Questo messaggio
    /close --> la stazione piu vicina(attualmente solo il return del input)
    """)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    db = sqlite3.connect("../db/wether.db")
    try:
        cursor = db.cursor()
        querry = """SELECT IDSTAZ, Latitude, Longitude FROM CoordinateStazioni"""
        cursor.execute(querry)
        allStaz = cursor.fetchall()
    except sqlite3.Error as sqlerror:
        print("Error while connecting to sqlite", sqlerror)

    updater = Updater(config.KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", cloasest))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
    if db:
        db.close()


if __name__ == "__main__":
    main()
