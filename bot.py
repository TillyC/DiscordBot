import openai
import discord
import os

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

# specifying our server
GUILD = "{Tilly's-Server}"

# create an object that will control our discord bot
client = discord.Client(intents=discord.Intents.default())
openai.api_key = os.environ.get["API_KEY"]
DISCORD_TOKEN = os.environ.get["DISCORD_TOKEN"]
openai.api_base = os.environ.get["API_BASE"]
#get our bot online
#guild is another term for server
@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break
	# print out nice statment saying our bot is online (only in command prompt)
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	# this prevents inifinte loops of bot talking to bot
	# if author of the message is the bot, don't do anything
	if message.author == client.user:
		return
	# ignore @everyone mentions
	if message.mention_everyone:
		return
	# if the message mentions the bot, then do something
	elif client.user.mentioned_in(message): 
		response = openai.ChatCompletion.create(
			engine="GPT-4",
			messages=[
			{"role": "system", "content": "You are a helpful LED component that is part of an electronics circuit called circute. You have a kind, child friendly, excitable personality. You provide information about electronic circuits in an easy to understand way."},
			{"role": "user", "content": message.content}
			]
		)
		await message.channel.send(response.choices[0].message.content)

client.run(DISCORD_TOKEN)