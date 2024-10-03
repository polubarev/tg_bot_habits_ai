import telebot

# Replace 'YOUR_BOT_TOKEN' with the token you get from BotFather
API_TOKEN = '7204830998:AAHmDYlFTJwtcHG8JHbnHZ-Qnq7d1OEdG-8'

bot = telebot.TeleBot(API_TOKEN)


# This handler will respond to any text message with the same message (echo)
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


# Start polling (keep the bot running and listen for incoming messages)
bot.polling()
