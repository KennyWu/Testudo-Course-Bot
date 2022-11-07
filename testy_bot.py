# This example requires the 'message_content' intent.

import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run('OTMxNDIyNzUxMzA5MzMyNTYw.GuGyGD.7NlKK32N_jSJOLb9_G8Pqp5_Thz2Dofih0feME')