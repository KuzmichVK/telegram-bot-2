# main.py — BreadFast: бот показывает меню и передаёт заказы на кухню
import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()  # читает .env из корня репозитория

# id чата кухни (твой Telegram ID) — строка, как требует тест
kitchen_chat_id = "725856695"
# Экземпляр Updater; токен бота — из .env (секрет не хардкодим)
updater = Updater(token=os.environ["BOT_TOKEN"])
# URL меню из задания
menu_url = "https://practicumgrade.github.io/course-material/bakery-menu.json"

# Текст-подсказка (для /help, ответа на не-заказ и приветствия)
HELP_TEXT = "Начните сообщение с «Закажи», чтобы передать заказ на кухню."


def get_menu():
    """Получить меню из внешнего источника и вернуть его в читаемом виде"""
    response = requests.get(menu_url)
    response_json = response.json()
    names = []
    # JSON: {"positions": [{"name": "..."}, ...]} — собираем имена позиций
    for position in response_json["positions"]:
        names.append(position["name"])
    menu_prefix = "Сегодня в меню: "
    menu_names = ", ".join(names)
    menu = menu_prefix + menu_names
    return menu


def show_menu(update, context):
    chat_id = update.effective_chat.id
    message = get_menu()
    context.bot.send_message(chat_id, message)


def process_order(update, context):
    chat = update.effective_chat
    client_message = update.message.text
    if client_message.startswith("Закажи "):
        order_message_prefix = "Новый заказ: "
        # Пересылаем заказ на кухню
        context.bot.send_message(
            chat_id=kitchen_chat_id,
            text=order_message_prefix + update.message.text,
        )
        # Подтверждаем клиенту
        context.bot.send_message(
            chat_id=chat.id,
            text="Передали сообщение на кухню, приходите завтра "
            "за заказом в любое время!",
        )
    else:
        # Сообщение не похоже на заказ — объясняем, как пользоваться
        context.bot.send_message(
            chat_id=chat.id,
            text=HELP_TEXT,
        )


def send_help(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=HELP_TEXT,
    )


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([["/menu"]], resize_keyboard=True)
    # Приветствие с кнопкой /menu
    context.bot.send_message(
        chat_id=chat.id,
        text="Добро пожаловать в BreadFast, {}!".format(name),
        reply_markup=button,
    )
    # Меню
    context.bot.send_message(
        chat_id=chat.id,
        text=get_menu(),
    )
    # Подсказка, как сделать заказ
    context.bot.send_message(
        chat_id=chat.id,
        text=HELP_TEXT,
    )


# Команды — выше обработчика текста: команда тоже текст,
# и без этого порядка её перехватил бы MessageHandler.
updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(CommandHandler("menu", show_menu))
updater.dispatcher.add_handler(CommandHandler("help", send_help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, process_order))

# Запуск поллинга (на верхнем уровне модуля: тест мокает обе и ждёт
# по одному вызову start_polling и idle)
updater.start_polling()
updater.idle()
