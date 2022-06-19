import os
import telebot
import math
import responses as rp

from keep_alive import keep_alive
from datetime import datetime



#Telegram API
TGBOT_KEY = os.environ['tg_key']


#Free openAI tokens will expire on this date - it 
#300,000 tokens available in the free trial  
expiry_date = "2022-09-15"
current_date = datetime.today().strftime('%Y-%m-%d')
exp_msg = "AI Bot has expired! Thanks for checking me out!"

  
#Max tokens per query
token_limit = 40
t_usg = rp.getTokenUsage()
max_tokens=300000

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def countTokens(inpTxt):
    # 1 token is approximately equal to 4 characters ==> 0.25 tokens/char
    tokenCount = math.ceil(0.25*len(inpTxt))
    return tokenCount

def expiryCheck(currStr,expStr,tcount,tlimit):
  if currStr >= expStr or tcount >= tlimit:
    return True
  else:
    return False

keep_alive()
bot = telebot.TeleBot(TGBOT_KEY)

@bot.message_handler(commands=['start'])
def start(message):
  rp.updateBotStatus(True)
  if expiryCheck(current_date,expiry_date,t_usg,max_tokens):
    bot.send_message(message.chat.id,exp_msg)
  
  else:
    bot.send_message(message.chat.id,rp.intro())


@bot.message_handler(commands=['stop'])
def stop(message):
  rp.updateBotStatus(False)
  bot.send_message(message.chat.id,"Bot off. Type /start to run again.")
  

@bot.message_handler(commands=['help'])
def help(message):
  if expiryCheck(current_date,expiry_date,t_usg,max_tokens):
    bot.send_message(message.chat.id,exp_msg)
  else:
    bot.send_message(message.chat.id,rp.helper())

@bot.message_handler(commands=['usage'])
def usage(message):
  if expiryCheck(current_date,expiry_date,t_usg,max_tokens):
    bot.send_message(message.chat.id,exp_msg)
  
  else:
    curr_token_usage = rp.getTokenUsage()
    pct_token_usage = round((curr_token_usage/300000)*100,2)
    days_rem=days_between(current_date,expiry_date)
    statmsg = f"Current Token Usage is {curr_token_usage} / 300,000 ({pct_token_usage}%).\
              \nDays remaining: {days_rem}"
    print(curr_token_usage)
    bot.send_message(message.chat.id,statmsg)


@bot.message_handler(func=lambda message: True)
def responder(message):
  query = message.text
  tokens = countTokens(query)
  
  if expiryCheck(current_date,expiry_date,t_usg,max_tokens):
    bot.send_message(message.chat.id,exp_msg)
  elif query[0]=="/":
    bot.reply_to(message,"That doesn't work you goof!")
      
  else:
    print(query)

    if rp.getBotStatus():
      bot.send_message(message.chat.id,rp.sample_responses(query,tokens,token_limit))

bot.polling()