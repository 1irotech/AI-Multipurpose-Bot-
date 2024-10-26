# import telebot
# from config import BOT_TOKEN, SECRET_KEY, API_KEY
# from logic import *
# from logic import Text2ImageAPI

# bot = telebot.TeleBot(BOT_TOKEN)

# # Данные по стилям
# styles_data = [
#     {"name": "DEFAULT", "title": "Default", "image": "https://cdn.fusionbrain.ai/static/download/img-style-personal.png"},
#     {"name": "UHD", "title": "Detailed Photo", "image": "https://cdn.fusionbrain.ai/static/download/img-style-detail-photo.png"},
#     {"name": "ANIME", "title": "Anime", "image": "https://cdn.fusionbrain.ai/static/download/anime-new.jpg"},
#     {"name": "KANDINSKY", "title": "abstract", "image": "https://cdn.fusionbrain.ai/static/download/img-style-kandinsky.png"}
# ]

# # Словарь для хранения выбранного стиля для каждого пользователя
# user_style_choice = {}

# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message, """\
# Hi there, I can generate videos and images based on your prompt, 
# summarize youtube videos and answer your questions in conversational format!\
# """)


# # Команда для выбора стиля
# @bot.message_handler(commands=['generate'])
# def text_to_image(message):
#     prompt = telebot.util.extract_arguments(message.text)

#     # Отправляем клавиатуру с кнопками выбора стиля
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     for style in styles_data:
#         button = telebot.types.InlineKeyboardButton(text=style['title'], callback_data=f"style:{style['name']}")
#         keyboard.add(button)

#     bot.send_message(message.chat.id, "Choose a style:", reply_markup=keyboard)

#     # Сохраняем промпт, чтобы потом использовать его при генерации
#     user_style_choice[message.chat.id] = {"prompt": prompt, "style": None}


# # Обработка выбора стиля
# @bot.callback_query_handler(func=lambda call: call.data.startswith('style:'))
# def handle_style_choice(call):
#     style = call.data.split(':')[1]
#     user_id = call.message.chat.id

#     # Обновляем информацию о выбранном стиле для данного пользователя
#     if user_id in user_style_choice:
#         user_style_choice[user_id]["style"] = style

#         # Генерация изображения после выбора стиля
#         prompt = user_style_choice[user_id]["prompt"]
#         api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)

#         model_id = api.get_model()

#         # Генерация изображения с выбранным стилем
#         uuid = api.generate(prompt, model_id, style=style)
#         images = api.check_generation(uuid)[0]

#         # Сохранение и отправка изображения
#         api.save_image(images, 'result.jpg')

#         with open('result.jpg', 'rb') as photo:
#             bot.send_photo(call.message.chat.id, photo)

#         bot.send_message(call.message.chat.id, "Here's your image with the chosen style!")

#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
#     else:
#         bot.send_message(call.message.chat.id, "Something went wrong, please try again.")

# bot.infinity_polling()

# Исправляем ошибку с некорректным использованием обратной косой черты в строке

import telebot
from config import BOT_TOKEN, SECRET_KEY, API_KEY
from logic import *
from logic import Text2ImageAPI
from deeppavlov import build_model, configs

# Загружаем модель DeepPavlov для вопросов и ответов
qa_model = build_model(configs.squad.squad, download=True)

bot = telebot.TeleBot(BOT_TOKEN)

# Данные по стилям
styles_data = [
    {"name": "DEFAULT", "title": "Default", "image": "https://cdn.fusionbrain.ai/static/download/img-style-personal.png"},
    {"name": "UHD", "title": "Detailed Photo", "image": "https://cdn.fusionbrain.ai/static/download/img-style-detail-photo.png"},
    {"name": "ANIME", "title": "Anime", "image": "https://cdn.fusionbrain.ai/static/download/anime-new.jpg"},
    {"name": "KANDINSKY", "title": "abstract", "image": "https://cdn.fusionbrain.ai/static/download/img-style-kandinsky.png"}
]

# Словарь для хранения выбранного стиля для каждого пользователя
user_style_choice = {}

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, (
        "Hi there, I can generate videos and images based on your prompt, "
        "summarize youtube videos and answer your questions in conversational format!"
    ))

# Команда для выбора стиля
@bot.message_handler(commands=['generate'])
def text_to_image(message):
    prompt = telebot.util.extract_arguments(message.text)

    # Отправляем клавиатуру с кнопками выбора стиля
    keyboard = telebot.types.InlineKeyboardMarkup()
    for style in styles_data:
        button = telebot.types.InlineKeyboardButton(text=style['title'], callback_data=f"style:{style['name']}")
        keyboard.add(button)

    bot.send_message(message.chat.id, "Choose a style:", reply_markup=keyboard)

    # Сохраняем промпт, чтобы потом использовать его при генерации
    user_style_choice[message.chat.id] = {"prompt": prompt, "style": None}


# Обработка выбора стиля
@bot.callback_query_handler(func=lambda call: call.data.startswith('style:'))
def handle_style_choice(call):
    style = call.data.split(':')[1]
    user_id = call.message.chat.id

    # Обновляем информацию о выбранном стиле для пользователя
    if user_id in user_style_choice:
        user_style_choice[user_id]['style'] = style

    # Генерация изображения с учетом выбранного стиля
    prompt = user_style_choice[user_id]['prompt']
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id, style=style)
    images = api.check_generation(uuid)[0]

    # Сохраняем и отправляем изображение пользователю
    api.save_image(images, 'result.jpg')
    with open('result.jpg', 'rb') as photo:
        bot.send_photo(call.message.chat.id, photo)


# Команда для вопросов с использованием DeepPavlov
@bot.message_handler(commands=['ask'])
def ask_question(message):
    question = telebot.util.extract_arguments(message.text)

    if not question:
        bot.reply_to(message, "Please provide a question after the /ask command.")
        return

    # Получаем ответ от модели DeepPavlov
    context = "..."  # Здесь можно добавить контекст или оставить пустым для простых вопросов
    answer = qa_model([context], [question])[0]

    # Отправляем ответ пользователю
    bot.reply_to(message, answer)


if __name__ == '__main__':
    bot.polling(none_stop=True)
