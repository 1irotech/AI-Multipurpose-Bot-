import telebot
from config import BOT_TOKEN
from logic import * 

bot = telebot.TeleBot(BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I can generate videos and images based on your prompt, 
summarize youtube videos and answer your questions in conversational format!\
""")

# @bot.message_handler(func=lambda message: True)
# def text_to_image(message):
#     prompt = message.text
#     api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
#     model_id = api.get_model()
#     uuid = api.generate(prompt, model_id)
#     images = api.check_generation(uuid)[0]

#     api.save_image(images, 'result.jpg')

#     with open('result.jpg', 'rb') as photo:
#         bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['generate'])
def text_to_image(message):
    prompt = message.text
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]

    api.save_image(images, 'result.jpg')

    with open('result.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.infinity_polling()