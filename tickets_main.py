import discord
import os
import asyncio
import traceback
import aioredis
from discord.ext import commands
from classes.io import JSONHandler

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.members = True

TOKEN = os.getenv("DISCORD_BOSONS_TESTS")
data_options = JSONHandler.read_json('json_files/options.json')

class SupportBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, application_id: int):
		super().__init__(command_prefix="$", intents=intents, application_id=application_id)
		self.redis = None

	async def setup_hook(self):
		await self.load_extension('classes.support')
		await self.load_extension('classes.creator')
		self.redis = aioredis.from_url("redis://localhost")

	async def on_ready(self):
		print(f'Cliente logado como {self.user} (ID: {self.user.id})')
			
				
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send('Command not found.')
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send('This command is on cooldown, try again later.')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('You do not have permission to use this command.')
		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.send('I do not have the required permissions to execute this command.')
		else:
			data_options = JSONHandler.read_json('json_files/options.json')
			log_channel = ctx.guild.get_channel(data_options["bot_configs"]["channel_bot_erro"]) #Canal de logs de erros

			traceback_message = ''.join(traceback.format_exception(None, error, error.__traceback__))
			await log_channel.send(f'Unexpected error:\n```\n{traceback_message}\n```')

bot = SupportBot(intents=intents, application_id=data_options["bot_configs"]["client_id"])

async def main():
	async with bot:
		await bot.start(TOKEN)

asyncio.run(main())
