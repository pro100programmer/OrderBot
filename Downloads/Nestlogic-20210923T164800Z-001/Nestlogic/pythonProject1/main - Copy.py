import logging
from typing import Dict
import db
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, chat, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery

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

reg_i = 0
reg_point_list = ["Name ", "Surname ", "Address ", "Phone number"]
clt_list = []
# Этот модуль определяет функции и классы, которые реализуют гибкую систему регистрации событий для приложений и библиотек
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
# Создание фаз для диалогов
START, TOKEN, TEXT, CHK_TOKEN, ORDER, GET_NUM = range(6)
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)


def integer_to_english(number):
    if number >= 1 and number <= 1000:
        a = ['', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE',
             'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN', 'TWENTY']
        if number <= 20:
            if number % 10 == 0:
                return a[number]
            else:
                return a[number]


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


# регистрация после ввода токена
def clt_start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Hi! Enter registration code pls and then write enter",
        reply_markup=ReplyKeyboardMarkup(keyboard_state(2)),
    )


# $######################################$###############################################$##############################################
# начало заказа
def reg_start(update: Update, context: CallbackContext) -> int:
    global reg_i, clt_list

    clt_list = []
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data=str(FOUR)),
            InlineKeyboardButton("No", callback_data=str(FIVE)),
        ],
    ]
    update.message.reply_text("Do you have registration code? ", reply_markup=InlineKeyboardMarkup(keyboard))

    return TOKEN


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

    keyboard = []
    update.callback_query.message.edit_text("You order has been successfully registered",
                                            reply_markup=InlineKeyboardMarkup(keyboard))

    return ConversationHandler.END

'''
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
        ],Blin pap
        [
            InlineKeyboardButton("Finish", callback_data=str(EIGHT)),
        ]
    ]
    update.callback_query.message.edit_text("So far you ordered: " + res, reply_markup=InlineKeyboardMarkup(keyboard))

    # while (i !=len
    return CHOISE2

'''
'''
# $###############################################$###############################################$###############################################$##############################################

# Подтверджение выбора 1
def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Please enter your {text.lower()}')

    


# Подтверджение выбора 2
def clt_reg(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Please enter your {text.lower()}')

    


# Введите токен
def token_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    update.message.reply_text(f'Please enter your token')
 


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
'''


def reg_yes(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global reg_i, reg_point_list
    keyboard = []

    query = update.callback_query

    query.answer()
    if reg_i < 4:
        query.edit_message_text(text='Please enter your ' + reg_point_list[reg_i],
                                reply_markup=InlineKeyboardMarkup(keyboard))
        reg_i += 1
        return TEXT
    else:
        keyboard = [
            [
                InlineKeyboardButton("Start", callback_data=str(SIX)),
            ]
        ]
        query.edit_message_text(text=f'You finished registering.\n'
                                     'By pressing the button you can start ordering',
                                reply_markup=InlineKeyboardMarkup(keyboard))

        return ORDER


def get_clt_data(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global clt_list

    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {int(query.data)}"
                                 "Please enter the information")

    clt_list.append(query.data)
    return TEXT
'''

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

    return CHOISE
'''

def data(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global reg_i, reg_point_list, clt_list
    chat_id = update.message.chat_id
    text = update.message.text

    clt_list.append(text)

    keyboard = [
        [
            InlineKeyboardButton("Enter", callback_data=str(ONE)),
            InlineKeyboardButton("Change", callback_data=str(TWO)),
            InlineKeyboardButton("Cancel", callback_data=str(THREE)),
        ]
    ]

    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    return START


def chk_token(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global reg_i, reg_point_list
    chat_id = update.message.chat_id
    text = update.message.text

    # update.message.reply_text("You entered: " + str(text))

    if db.if_token_exists(text) == 1:

        keyboard = [
            [
                InlineKeyboardButton("Start", callback_data=str(ONE))
            ]
        ]

        update.message.reply_text("Start registering", reply_markup=InlineKeyboardMarkup(keyboard))

        return START
    else:
        update.message.reply_text("Please ask for a valid reg code and start again")
        return ConversationHandler.END


def token_notif_yes(update: Update, context: CallbackContext) -> None:
    keyboard = []
    update.callback_query.message.edit_text("Please enter the code ", reply_markup=InlineKeyboardMarkup(keyboard))
    return CHK_TOKEN


def token_notif_no(update: Update, context: CallbackContext) -> None:
    keyboard = []
    update.callback_query.message.edit_text("Please contact the owner for a code and start again",
                                            reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END


def cancel_operation(update: Update, context: CallbackContext) -> None:
    keyboard = []
    update.callback_query.message.edit_text("You canceled this action. You can start again when you want.",
                                            reply_markup=InlineKeyboardMarkup(keyboard))
    return ORDER


def change_data(update: Update, context: CallbackContext) -> None:
    global clt_list
    clt_list.remove(clt_list[-1])

    keyboard = []
    update.callback_query.message.edit_text("Enter what your new change ", reply_markup=InlineKeyboardMarkup(keyboard))
    return TEXT


def want_order(update: Update, context: CallbackContext) -> None:
    keyboard = []
    keyboard.append([InlineKeyboardButton("Yes", callback_data=str(NINE))])
    keyboard.append([InlineKeyboardButton("No", callback_data=str(SEVEN))])
    update.callback_query.message.reply_text("Do you wish to order? ", reply_markup=InlineKeyboardMarkup(keyboard))
    return ORDER


def choose_ord(update: Update, context: CallbackContext) -> None:
    global sup_list, ordkeyboard
    sup_list = db.get_sup()
    ordkeyboard = [[]]

    for i in range(len(sup_list)):
        ordkeyboard[0].append(InlineKeyboardButton(sup_list[i][0], callback_data=str(sup_list[i][0])))

    update.callback_query.message.edit_text("What do you wish to order",
                                            reply_markup=InlineKeyboardMarkup(ordkeyboard))
    return ORDER


def amt(update: Update, context: CallbackContext) -> None:
    global sup_list, ordkeyboard
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: " + str(db.get_choise()[0][0]) +

                                 " Please enter the information")
    db.drop_choice()
    clt_list.append(query.data)


def main() -> None:
    global registration_state, security, markup, conv_handler2, keybrd_state, reg_2
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("
                 ")
    reg_1 = db.get_ids()

    # Get the dispatcher to register handlers
    # filters.Filters.chat.add_chat_ids(12345678)
    dispatcher = updater.dispatcher
    check = MessageHandler(Filters.regex('[a-zA-Z0-9]'), get_name)
    prd = db.get_sup()

    vs = [CallbackQueryHandler("Start", want_order, pattern='^' + str(SIX) + '$'),
          CallbackQueryHandler("No", cancel_operation, pattern='^' + str(SEVEN) + '$'),
          CallbackQueryHandler("Yes", choose_ord, pattern='^' + str(NINE) + '$'),
          ]
    for i in range(len(prd)):
        vs.append(CallbackQueryHandler(prd[i][0], amt, pattern='^' + str(prd[i][0]) + '$'))
        print(prd[i][0])
    registration = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^/start$'), reg_start)],
        states={
            START: [
                CallbackQueryHandler("Enter", reg_yes, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler("Change", change_data, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler("cancel", cancel_operation, pattern='^' + str(THREE) + '$'),
            ],
            TEXT: [
                MessageHandler(Filters.regex('[a-zA-Z0-9]'), data),
            ],
            TOKEN: [
                CallbackQueryHandler("Yes", token_notif_yes, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler("No", token_notif_no, pattern='^' + str(FIVE) + '$'),
            ],
            CHK_TOKEN: [
                MessageHandler(Filters.regex("[0-9]+$"), chk_token),
            ],
            ORDER: vs,
            GET_NUM: [
                MessageHandler(Filters.regex("[0-9]+$"), amt),
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done'), ord_end)],

    )
    # dispatcher.add_handler(check, 0)

    dispatcher.add_handler(registration, 1)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


###
if __name__ == '__main__':
    main()
