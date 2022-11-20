from telegram.ext import *
import keys
import pandas_datareader as web

#Init
print ("Starting up SabarobeBot...")

#Funciones
def start_command(update, context):
    update.message.reply_text("Welcome to SabarobeBot")

def stock_command(update, context):
    ticker = context.args[0]
    data = web.DataReader(ticker, 'yahoo')
    price = data.iloc[-1]['Close']
    update.message.reply_text(f"The current price of {ticker} is {price:.2f}$!")

def contact_command(update, context):
    update.message.reply_text("http://www.sabarobestudios.io")

def help_command(update, context):
    update.message.reply_text("""
    Help Menu
    /start -> Start the Bot
    /stock -> Stock price: /stock + ticker
    /contact -> Information about contact
    /help -> Help menu

    """)


def handle_response(text: str) -> str:
    if "hello" in text:
        return "hey there"

    if "Sabarobe" in text:
        return "arre"
    
    if "help" in text:
        return "Helping"


    return "invalid message"

def handle_message(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ""

    print(f'User ({update.message.chat.id}) says: "{text}" in {message_type}')

    
    if message_type == "group":
        if "@sabarobebot" in text:
            new_text = text.replace("@sabarobebot", "").strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    update.message.reply_text(response)

def error(update, context):
    print(f'Update ({update}) caused error: {context.error}')


if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    #Command
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('stock', stock_command))
    dp.add_handler(CommandHandler('contact', contact_command))
    dp.add_handler(CommandHandler('help', help_command))
    

    #Message
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    #error
    dp.add_error_handler(error)

    #Run Bot
    updater.start_polling() 
    updater.idle()   

