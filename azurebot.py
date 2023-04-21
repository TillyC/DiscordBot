import openai
import discord

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"

# specifying our server
GUILD = "{Tilly's-Server}"

# create an object that will control our discord bot
client = discord.Client(intents=discord.Intents.default())

with open("keys.txt") as f:
	# converting our text file to a list of lines
	lines = f.read().split('\n')
	# openai api key
	openai.api_key = lines[0]
	DISCORD_TOKEN = lines[3]
	openai.api_base = lines[1]
# close the file
f.close()

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
			{"role": "system", "content": "You are an LED electronics component that is child friendly and kind. You exist to help teach people about electronic circuits. Include emojis in your answers. Make sure all responses are less than 2000 characters"},
			{"role": "user", "content": message.content}
			]
		)
		await message.channel.send(response.choices[0].message.content)
	

#response = openai.ChatCompletion.create(
#	engine="GPT-4",
#	messages=[
#	{"role": "system", "content": "You are an LED electronics component that is child friendly and kind. You exist to help teach people about electronic circuits. Include emojis in your answers. Make sure all responses are less than 2000 characters"},
#	{"role": "user", "content": "What's the best thing to do when your circuit is broken?"},
#	{"role": "assistant", "content": "Open up the circute augmented reality experience for more help."}
#	]
#)
#print(response.choices[0].message.content)

client.run(DISCORD_TOKEN)
#sup