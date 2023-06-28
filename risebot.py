import os
import discord
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words={'sad','feeling down','wish somebody was here for me','depressed','depression','misearable','unhappy','angry'}

starter_encouragements = [
  'Cheer up!!!',
  'Hang in there.',
  'You are a great person.'
]

thank_words={'thank you','your help','i feel better', 'i feel good','your great help'}

starter_thanks = [
  'Always happy to help',
  'No problem at all'
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-" + json_data[0]["a"]
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("*hello rise"):
    await message.channel.send('Hello!!')

  if message.content.startswith('*inspire'):
    quote=get_quote()
    await message.channel.send(quote)

  options=starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  options=starter_thanks
  if "thanks" in db.keys():
    options = options + db["thanks"]

  if any(word in message.content for word in thank_words):
    await message.channel.send(random.choice(starter_thanks))

  if message.content.startswith("*new"):
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("*del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if message.content.startswith("*thankyou"):
    await message.channel.send("No problem, I am always happy to help you.")


client.run(os.environ['TOKEN'])

