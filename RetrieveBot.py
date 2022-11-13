# This example requires the 'message_content' intent.

import discord

discord.utils.setup_logging()


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run('OTMxNDIyNzUxMzA5MzMyNTYw.GNOTJH.6vG18RHSbNRTrG-c8mZr29OuhYcsUnHSFQdoQs')
