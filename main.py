import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6546065956:AAGaXmEEo5mSqhypzkOq2UDxBFWWP6V71DU",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Когда отменяем Новый Год"  # Можно менять текст
text_button_1 = "30 декабря"  # Можно менять текст
text_button_2 = "31 декабря"  # Можно менять текст
text_button_3 = "1 января"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'привет! много не знаю, еСть ПАру команд С веба, тИпа run, link. нЕмНого ржаки, нЕмНого смыслА. надеюсь бот Воркает вот... кому Интересно котик (ЖУк) с авы бота Мой. люблю Его! (правДа, крутой?). пройди регистрацию!',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! [Ваш](https://www.example.com/) `возраст?`')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за регистрацию! Теперь вы внесены в список Плохих Детей за желание отменить Новый Год!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Без права на реабилитацию!", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "СОВСЕМ. Подарков тоже не будет. Дед Мороз обиделся! ;-( ", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Okey-dokey, this is a joke! (немного ражаки, немного английского) Вы не в черном списке и подарки будут. Поздравляем Вас с приближением самого радостного, доброго, волшебного праздника — Нового года! Пусть этот год станет чередой счастливых и радостных дней, наполненных любовью, добром и верой в лучшее! (вызови /link)", reply_markup=menu_keyboard)  # Можно менять текст

@bot.message_handler(commands=['link'])
def main(message):
    bot.send_message(message.chat.id, '[ССЫЛКА](https://www.youtube.com/watch?v=E8gmARGvPlI)', parse_mode='Markdown')

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

