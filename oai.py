import os
import openai

OAI_KEY = os.environ['openai_key']


def gpt3(txt,tokenLimit,aiEngine=0):
  openai.api_key = OAI_KEY
  
  #engine list
  aiEngineList = ("text-ada-001","text-babbage-001","text-curie-001","text-davinci-002")

  response = openai.Completion.create(
    engine=aiEngineList[aiEngine],
    prompt=txt,
      temperature=0.7,
      max_tokens=tokenLimit,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )
  
  return response.choices[0].text
  
