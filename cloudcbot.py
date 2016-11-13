import telegram
import TOKENS
from time import sleep
from random import randint

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError

def main():
    
    global LAST_UPDATE_ID
    
    bot = telegram.Bot(TOKENS.TOKEN);
    
    print 'Starting Cloud Computing Bot...'

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        try:
            cloudcbot(bot)
        except telegram.TelegramError as e:
            if e.message in ("Bad Gateway", "Timeout"):
                sleep(5)
            else:
                raise e
        except URLError as e:
            sleep(5)

def cloudcbot(bot):

    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset = LAST_UPDATE_ID, timeout = 10):
        chat_id = update.message.chat_id
        message = update.message.text
        args = message.split(" ")
        size = len(args);

        if args[0] == "/google" or args[0] == "/google@cloudcbot_bot":
            if size > 1:
                res = 'http://lmgtfy.com/?q='

                for i in range(1, size):
                    res = res + args[i]
                    if i < size - 1:
                        res = res + '+'
                bot.sendMessage(chat_id = chat_id, text = res)
            else:
                res = 'http://lmgtfy.com/?q=google'
                bot.sendMessage(chat_id = chat_id, text = res)

        elif args[0] == "/help" or args[0] == "/help@cloudcbot_bot":
            if size == 1:
                msg = "Available commands:\n\n\
/help [command]* - Command to show some help about the the bot or other \
available commands\n\n \
/google [text] - Will generate a Let Me Google That For You link\n\n\n \
*Optional arguments\n"
                print chat_id
                bot.sendMessage(chat_id = chat_id, text = msg)
            elif size == 2:
                if args[1] == 'help':
                    msg = '/help help - Some help for cloudcbot users'
                elif args[1] == 'google':
                    msg = '/google word1 word2 ...  - Will generate a LMGTFY to \
help your friend'
                else:
                    msg = 'Invalid command! (try again)'

                bot.sendMessage(chat_id = chat_id, text = msg)

            bot.sendMessage(chat_id = chat_id, text = msg)

        LAST_UPDATE_ID = update.update_id + 1        

if __name__ == '__main__':
    main()
