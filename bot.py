import telegram

bot = telegram.Bot(token='5339286582:AAHy4w-c0KZZ7ntZ6HF_gpwDGv1OGQSUVTk')
# print(bot.get_me())

# updates = bot.get_updates()

# bot.send_message(chat_id='@spacex_and_nasa_photo_channel', text='какой-нибудь текст в канал')
bot.send_document(chat_id='@spacex_and_nasa_photo_channel', document=open('images/nasa_apod/nasa_apod_1.gif', 'rb'))