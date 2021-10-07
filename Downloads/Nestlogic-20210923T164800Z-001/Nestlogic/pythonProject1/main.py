import logging
from typing import Dict
import db
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, chat, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,

)

registration_state = False
security = True
state = 1
keybrd_state = 1
reg_2 = []
what_to_order = []
# Этот модуль определяет функции и классы, которые реализуют гибкую систему регистрации событий для приложений и библиотек
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
# Создание фаз для диалогов
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
CHOOSING2, TYPING_REPLY2, TYPING_CHOICE2 = range(3)
CHOISE, CHOISE2, HOW_MUCH, TEXT, TYPING_REPLY3, TYPING_CHOICE3 = range(6)
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT = range(8)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# Создание состояний клавиатуры для ввода
def keyboard_state(state: int):
    if state == 1:
        reply_keyboard = [
            ['Token', 'Enter']
        ]
    if state == 2:
        reply_keyboard = [
            ['Name', 'Surname', 'Address'],
            ['Done'],
        ]
    if state == 3:
        reply_keyboard = [
            ['Welcome back'],
        ]
    return reply_keyboard


# Перевод словаря в строку
def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


# Узнавание пользователя
def get_name(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    if len(db.get_name(chat_id)) != 0:
        name = db.get_name(chat_id)[0][0]

        update.message.reply_text("Hi! " + str(name))


# Начало регистрации
def start_reg(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! Enter registration code pls and then write enter",
        reply_markup=ReplyKeyboardMarkup(keyboard_state(1)),
    )

    return CHOOSING


# регистрация после ввода токена
def clt_start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Hi! Enter registration code pls and then write enter",
        reply_markup=ReplyKeyboardMarkup(keyboard_state(2)),
    )

    return CHOOSING2


# $######################################$###############################################$##############################################
# начало заказа
def order_start(update: Update, context: CallbackContext) -> int:
    global items, prd_list, lst, clt_list
    lst = ''
    items = []
    for i in range(len(db.get_sup())):
        lst = lst + db.get_sup()[i][0] + '-' + str(i + 1) + '\n'
        items.append(db.get_sup()[i][0])
    db.get_sup()
    prd_list = []
    clt_list = []
    keyboard = [
        [
            InlineKeyboardButton("Yogurt", callback_data=str(ONE)),
            InlineKeyboardButton("Milk", callback_data=str(TWO)),
            InlineKeyboardButton("Honey", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton("Next", callback_data=str(FOUR)),
        ],
    ]

    update.message.reply_text(lst, reply_markup=InlineKeyboardMarkup(keyboard))

    return CHOISE


'''
# Список продуктов
def ord_reg(update: Update, context: CallbackContext) -> int:
    global what_to_order, items, d_items
    text = update.message.text

    d_items = {}
    for i, item in enumerate(items):
        d_items[i + 1] = item


    return TYPING_REPLY3
'''


def ord_end(update: Update, context: CallbackContext) -> int:
    global clt_list

    print(clt_list)
    keyboard = []
    update.callback_query.message.edit_text("You order has been successfully registered",
                                            reply_markup=InlineKeyboardMarkup(keyboard))

    return ConversationHandler.END


# Конец заказа
def next(update: Update, context: CallbackContext) -> int:
    global what_to_order, d_items, prd_list
    d_items = {}
    ord_id = 0
    ord_id = db.get_rand()
    for i, item in enumerate(items):
        d_items[i] = item
    res = ''
    for i in range(len(prd_list) // 2):
        res = res + str(d_items[prd_list[i * 2]]) + " : " + str(prd_list[i * 2 + 1]) + " "
        db.add_to_ordered_supplies(ord_id, prd_list[i * 2], prd_list[i * 2 + 1])
    keyboard = [
        [
            InlineKeyboardButton("Address", callback_data=str(FIVE)),
            InlineKeyboardButton("Phone number", callback_data=str(SIX)),
            InlineKeyboardButton("Notes", callback_data=str(SEVEN)),
        ],
        [
            InlineKeyboardButton("Finish", callback_data=str(EIGHT)),
        ]
    ]
    update.callback_query.message.edit_text("So far you ordered: " + res, reply_markup=InlineKeyboardMarkup(keyboard))


    # while (i !=len
    return CHOISE2


# $###############################################$###############################################$###############################################$##############################################

# Подтверджение выбора 1
def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Please enter your {text.lower()}')

    return TYPING_REPLY


# Подтверджение выбора 2
def clt_reg(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Please enter your {text.lower()}')

    return TYPING_REPLY2


# Введите токен
def token_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    update.message.reply_text(f'Please enter your token')
    return TYPING_REPLY


# Подтверджение токена
def received_token(update: Update, context: CallbackContext) -> int:
    global registration_state, security, gtoken
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Check if everything is correct:"
        f"{facts_to_str(user_data)}",

        reply_markup=ReplyKeyboardMarkup(keyboard_state(1)),
    )

    return CHOOSING


# Подтверджение регистрации клиента
def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Check the token"
        f"{facts_to_str(user_data)}",

        reply_markup=ReplyKeyboardMarkup(keyboard_state(2)),
    )

    return CHOOSING2


# закончить регистрацию клиента
def done_reg(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"You were successfully registered {facts_to_str(user_data)}",

    )
    status = "Customer"
    db.add_to_Clients(user_data["Name"], user_data["Surname"], user_data["Address"], chat_id, status)

    user_data.clear()
    return ConversationHandler.END


# закончить подтверждение токена
def end_sec(update: Update, context: CallbackContext) -> int:
    global registration_state, security, markup, conv_handler2, reg_2
    user_data = context.user_data
    chat_id = update.message.chat_id
    if 'choice' in user_data:
        del user_data['choice']

    if isfloat(user_data["Token"]):
        if db.if_token_exists(user_data["Token"]) == 1:
            user_data.clear()
            reg_2.append(chat_id)
            update.message.reply_text(
                f"Press the button to start registering{facts_to_str(user_data)}",
                reply_markup=ReplyKeyboardMarkup([['Register']])

            )

        else:
            update.message.reply_text("Wrong token, please restart the bot")
            user_data.clear()
            return ConversationHandler.END
    # markup = ReplyKeyboardMarkup(keyboard_state(2))
    # reply_markup = markup
    else:
        update.message.reply_text("Wrong token, please restart the bot")
        user_data.clear()
        return ConversationHandler.END


def get_ord_data(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global prd_list

    prd_id = 0
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {int(query.data) + 1}"
                                 "Enter how much of item do you want")

    prd_id = int(query.data)
    prd_list.append(prd_id)
    return HOW_MUCH


def get_clt_data(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global clt_list

    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {int(query.data)}"
                                 "Please enter the information")

    clt_list.append(query.data)
    return TEXT


def amount(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global prd_list, lst

    text = update.message.text
    prd_amt = int(text)
    update.message.reply_text("You chose this amount: " + str(prd_amt))
    prd_list.append(prd_amt)
    keyboard = [
        [
            InlineKeyboardButton("Yogurt", callback_data=str(ONE)),
            InlineKeyboardButton("Milk", callback_data=str(TWO)),
            InlineKeyboardButton("Honey", callback_data=str(THREE)),
        ],
        [
            InlineKeyboardButton("Next", callback_data=str(FOUR)),
        ]
    ]

    update.message.reply_text(lst, reply_markup=InlineKeyboardMarkup(keyboard))
    print(prd_list)
    return CHOISE


def data(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global clt_list
    chat_id = update.message.chat_id
    text = update.message.text

    update.message.reply_text("You entered: " + str(text))
    clt_list.append(text)
    keyboard = [
        [
            InlineKeyboardButton("Address", callback_data=str(FIVE)),
            InlineKeyboardButton("Phone number", callback_data=str(SIX)),
            InlineKeyboardButton("Notes", callback_data=str(SEVEN)),
        ],
        [
            InlineKeyboardButton("Finish", callback_data=str(EIGHT)),
        ]
    ]

    update.message.reply_text(lst, reply_markup=InlineKeyboardMarkup(keyboard))
    print(clt_list)

    return CHOISE2


'''

def order(update: Update, _: CallbackContext) -> None:
    keyboard = [
        InlineKeyboardButton(str(db.get_sup()), callback_data='idk'),
    ]

    reply_markup = InlineKeyboardMarkup([[button]*5 for button in keyboard*len(db.get_sup())])
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")
'''


def main() -> None:
    global registration_state, security, markup, conv_handler2, keybrd_state, reg_2
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1760508363:AAG9wpxa-B3JsNcQtQ1kolqClERXxn099MU")
    reg_1 = db.get_ids()

    # Get the dispatcher to register handlers
    # filters.Filters.chat.add_chat_ids(12345678)
    dispatcher = updater.dispatcher
    check = MessageHandler(Filters.regex('[a-zA-Z0-9]'), get_name)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler((~ Filters.chat(reg_1[0])) & Filters.regex('^start$'), start_reg)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^Token$'), regular_choice
                ),

            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Enter$')), regular_choice
                ),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Enter$')),
                    received_token,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Enter$'), end_sec)],

    )

    conv_handler2 = ConversationHandler(
        entry_points=[MessageHandler((~ Filters.chat(reg_1[0])) & Filters.regex('^Register$'), clt_start)],
        states={
            CHOOSING2: [
                MessageHandler(
                    Filters.regex('^(Name|Surname|Address)$'), clt_reg
                ),

            ],
            TYPING_CHOICE2: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), clt_reg
                ),
            ],
            TYPING_REPLY2: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done'), done_reg)],
    )
    conv_handler3 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Order$'), order_start)],
        states={
            CHOISE: [

                CallbackQueryHandler(get_ord_data, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(get_ord_data, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(get_ord_data, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(next, pattern='^' + str(FOUR) + '$'),
            ],
            CHOISE2: [
                CallbackQueryHandler(get_clt_data, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(get_clt_data, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(get_clt_data, pattern='^' + str(SEVEN) + '$'),
                CallbackQueryHandler(ord_end, pattern='^' + str(EIGHT) + '$'),
            ],
            HOW_MUCH: [
                MessageHandler(Filters.regex("[0-9]+$"), amount),
            ],
            TEXT: [
                MessageHandler(Filters.regex("[a-zA-z0-9]"), data),
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done'), ord_end)],

    )
    # dispatcher.add_handler(check, 0)
    dispatcher.add_handler(conv_handler, 1)
    dispatcher.add_handler(conv_handler2, 2)
    dispatcher.add_handler(conv_handler3, 3)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


###
if __name__ == '__main__':
    main()
