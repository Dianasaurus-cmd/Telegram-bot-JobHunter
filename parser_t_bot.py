import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from parser_ru import *
from telegram.ext import ApplicationBuilder, CallbackQueryHandler,CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

from config import TOKEN,BOT_USERNAME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Привет! Я помогу тебе найти желаемую вакансию!")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = ' '.join(context.args).upper())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = 'Для дого чтобы посмотреть возможные команды, нажмите /')

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id,text = 'Команды не была распознана')

async def view_top_10_best_payed_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE,page_start = -1,tries = 0):
    print('started...')
    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"У вас осталось {7-tries} попыток.\nПодождите минутку, данные загружаются")
    text_send, page  = Search_for_jobes.view_top_10(page_start)
    for message_send in text_send:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = message_send[:4096])

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split(',')
    if (len(data) == 1 and data[0] == "2") or data[0] == "39":
        await  query.edit_message_text( text = "Хочешь ли ты продолжить другой поиск?")
    else:
        if data[2] == 'VIEW':
            await view_top_10_best_payed_jobs(update, context, int(data[1]),int(data[0])+1)
        elif data[2] == 'NAME':
            await load_names(update, context, int(data[1]),int(data[0])+1,data[3])
        elif data[2] == 'COMPANY':
            await load_company(update, context, int(data[1]),int(data[0])+1,data[3])
        elif data[2] == 'SALARY':
            await load_salary(update, context, int(data[1]),int(data[0])+1,data[3])
        elif data[2] == 'CITY':
            await load_city(update, context, int(data[1]),int(data[0])+1,data[3])

        

NAME, SALARY, COMPANY, CITY = range(4)

async def search_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Какую профессию ты бы хотела вернуть?")
    return NAME

async def load_names(update: Update, context: ContextTypes.DEFAULT_TYPE, page_start=-1,tries = 0,name_search = ""):
    if name_search == "":
        user_name = update.message.text
    else:
        user_name = name_search
    await context.bot.send_message(chat_id = update.effective_chat.id, text =f"Отлично! будем искать профессию по ключевому слову: {user_name}")
    print('started...')
    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"У вас осталось {39-tries} попыток.\nПодождите минутку, данные загружаются")
    text_send, page  = Search_for_jobs.search_name(user_name,page_start)
    for message_send in text_send:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = message_send[:4096])
    keyboard = [[InlineKeyboardButton("Загрузи информацию из других страниц", callback_data = f"{tries},{page},NAME,{user_name}")],[InlineKeyboardButton("Хватит", callback_data = "2") ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Хочешь продолжить или закончить поиск?",reply_markup = reply_markup)
    return ConversationHandler.END

async def search_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Какую компанию ты бы хотела вернуть?")
    return COMPANY

async def load_company(update: Update, context: ContextTypes.DEFAULT_TYPE, page_start=0,tries = 0,name_search = ""):
    print(name_search)
    if name_search == "":
        user_name = update.message.text
    else:
        user_name = name_search
    await context.bot.send_message(chat_id = update.effective_chat.id, text =f"Отлично! будем искать профессию по по компании: {user_name}")
    print('started...')
    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"У вас осталось {39-tries} попыток.\nПодождите минутку, данные загружаются")
    text_send, page  = Search_for_jobs.search_company(user_name,page_start)
    for message_send in text_send:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = message_send[:4096])
    keyboard = [[InlineKeyboardButton("Загрузи информацию из других страниц", callback_data = f"{tries},{page},COMPANY,{user_name}")],[InlineKeyboardButton("Хватит", callback_data = "2") ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Хочешь продолжить или закончить поиск?",reply_markup = reply_markup)
    return ConversationHandler.END

async def search_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Какую зарплату ты бы хотела вернуть?")
    return SALARY

async def load_salary(update: Update, context: ContextTypes.DEFAULT_TYPE, page_start=-1,tries = 0,name_search = ""):
    if name_search == "":
        user_name = update.message.text
    else:
        user_name = name_search
    await context.bot.send_message(chat_id = update.effective_chat.id, text =f"Отлично! будем искать профессию по ключевому слову: {user_name}")
    print('started...')
    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"У вас осталось {39-tries} попыток.\nПодождите минутку, данные загружаются")
    text_send, page  = Search_for_jobs.search_salary(user_name,page_start)
    for message_send in text_send:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = message_send[:4096])
    keyboard = [[InlineKeyboardButton("Загрузи информацию из других страниц", callback_data = f"{tries},{offset},SALARY,{user_name}")],[InlineKeyboardButton("Хватит", callback_data = "2") ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Хочешь продолжить или закончить поиск?",reply_markup = reply_markup)
    return ConversationHandler.END

async def search_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Какую город ты бы хотела вернуть?")
    return CITY

async def load_city(update: Update, context: ContextTypes.DEFAULT_TYPE, page_start=-1,tries = 0,name_search = ""):
    if name_search == "":
        user_name = update.message.text
    else:
        user_name = name_search
    await context.bot.send_message(chat_id = update.effective_chat.id, text =f"Отлично! будем искать профессию по городу: {user_name}")
    print('started...')
    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"У вас осталось {39-tries} попыток.\nПодождите минутку, данные загружаются")
    text_send, page  = Search_for_jobs.search_city(user_name,page_start)
    for message_send in text_send:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = message_send[:4096])
    keyboard = [[InlineKeyboardButton("Загрузи информацию из других страниц", callback_data = f"{tries},{page},CITY,{user_name}")],[InlineKeyboardButton("Хватит", callback_data = "2") ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Хочешь продолжить или закончить поиск?",reply_markup = reply_markup)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Спасиюо за доверие!")
    return ConversationHandler.END

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Error occured")
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Что-то пошло не так... попробуйте снова")

if __name__=="__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start',start)
    caps_handler = CommandHandler('caps',caps)
    help_handler = CommandHandler('help_command',help_command)
    view_top_10_best_payed_jobs_handler = CommandHandler('view_top_10_best_payed_jobs',view_top_10_best_payed_jobs )
    conv_handler_name = ConversationHandler(entry_points = [CommandHandler("search_name",search_name),CommandHandler("search_salary",search_salary),CommandHandler("search_company",search_company),CommandHandler("search_city",search_city)],
        states = {NAME: [MessageHandler(filters.TEXT,load_names)], COMPANY:[MessageHandler(filters.TEXT,load_company)],CITY:[MessageHandler(filters.TEXT,load_city)],SALARY:[MessageHandler(filters.TEXT,load_salary)]},
        fallbacks = [CommandHandler("cancel",cancel)])
    unknown_handler = MessageHandler(filters.COMMAND,unknown)
            #добавляем команды в бота

            
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(help_handler)
    application.add_handler(view_top_10_best_payed_jobs_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(conv_handler_name)
    application.add_error_handler(error)
    application.add_handler(unknown_handler)

            
    application.run_polling()
