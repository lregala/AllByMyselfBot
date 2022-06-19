from random import randrange
import oai
import math
from replit import db


def updateBotStatus(botstat):
  if "IsBotActive" in db.keys():
    db["IsBotActive"]=botstat
  else:
    db["IsBotActive"]=False


def getBotStatus():
  if "IsBotActive" in db.keys():
    botstat = db["IsBotActive"]
    return botstat 
  else:
    db["IsBotActive"]=False

def countTokens(inpTxt):
    # 1 token is approximately equal to 4 characters ==> 0.25 tokens/char
    tokenCount = math.ceil(0.25*len(inpTxt))
    return tokenCount

def updateTokenUsage(tcount):
  if "usedTokens" in db.keys():
    db["usedTokens"]+=tcount
  else:
    db["usedTokens"]=5917 #starting used tokens out of 300,000

def getTokenUsage():
  if "usedTokens" in db.keys():
    t_Usage = db["usedTokens"]
    return t_Usage 
  else:
    db["usedTokens"]=5917 #starting used tokens out of 300,000
    
def sample_responses(inpTxt,tcount,tlimit,ai_level):
  # included sample responses to not waste tokens
  
  defaultReplies = ["...","I didn't get that.","Say again?","Try again.","Hmm, I didn't catch that."]
  defaultComplaints = ["You talk too much!","blah blah blah","k","*yawn*","tl;dr"]
  defaultIntros =["Hey! I'm here to chat, in case you were feeling lonely.",\
                "Feeling lonely? I'm down to chat.",\
               "Here to chat. I won't judge you for talking to an inanimate object.",\
                "All by yourself? I'm here to chat.",\
                 "Need to pretend like you're texting someone? I'm here to help."]
  
  user_msg = str(inpTxt).lower()
  
  if user_msg in ("hi","hello","sup","yo","hey","wassup"):
      idx_randIntro = randrange(len(defaultIntros))
      return defaultIntros[idx_randIntro]
      

  elif tcount > tlimit:
      idx_randComp = randrange(len(defaultComplaints))
      return defaultComplaints[idx_randComp]
 
  elif tcount <=1:
      #idx_randReply = randrange(len(defaultReplies))
      return defaultReplies[0]
  else:
    #use gpt3 here
    try:
      resp = oai.gpt3(inpTxt,tlimit,ai_level)
      r_tcount=countTokens(resp)
      print(r_tcount)
      print(tcount)
      print(resp)
      
      updateTokenUsage(tcount+r_tcount)
      return resp
    except:
      return "Uh-oh, something went wrong!"
  
    
def intro():
  intro_str = "**********All By Myself Bot**********\n"
  body_str = "\nThis is an AI chatbot powered by OpenAI's GPT-3.\
              \n\nThis version of the bot is under the free plan,\
              \nwhich is only limited to three months of usage or 300,000 tokens. \n(1 token = 4 char)\
              \nThe AI will stop functioning after the free trial has ended."
              
  end_str = "\nNow, type something to get started..."

  
  return intro_str+body_str+end_str
  

def helper():
    helpstr="Available commands:\
            \n/help - list of available commands\
            \n/run - use a different engine for response, from 0-3. Higher is better.\
            \nDefault 0. example: run 3 create a shopping list out of 5 items.\
            \n/start - start the bot\
            \n/stop - stop the bot\
            \n/usage - see token usage and days remaining"
    return helpstr
