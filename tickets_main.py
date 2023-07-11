import discord
import os
import asyncio
import traceback
import aioredis
import datetime
from discord.ext import commands
from classes.io import JSONHandler
from classes.redis_handler import RedisHandler

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.members = True

TOKEN = os.getenv("DISCORD_BOSONS_TESTS")
data_options = JSONHandler.read_json('json_files/options.json')

class SupportBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, application_id: int):
		super().__init__(command_prefix=data_options["bot_configs"]["prefix"], intents=intents, application_id=application_id)
		self.redis = None
		self.redis_handler = None

	async def setup_hook(self):
		## Lendo as cogs
		await self.load_extension('classes.support')
		await self.load_extension('classes.creator')

		## Conectando ao servidor Redis
		self.redis = aioredis.from_url("redis://localhost")

		## Inicializando a classe RedisHandler com self.redis
		self.redis_handler = RedisHandler(self.redis)

	async def on_ready(self):
		print(f'Cliente logado como {self.user} (ID: {self.user.id})')
			
				
	async def on_command_error(self, ctx, error):
		await ctx.defer(ephemeral=True)
		if isinstance(error, commands.CommandNotFound):
			await ctx.send('> Comando não encontrado!', ephemeral=True)
		elif isinstance(error, commands.CommandOnCooldown):
			retry_after = error.retry_after  # Tempo restante em segundos
			tempo_restante = datetime.timedelta(seconds=retry_after)

			dias = tempo_restante.days
			horas, resto_segundos = divmod(tempo_restante.seconds, 3600)
			minutos, segundos = divmod(resto_segundos, 60)

			mensagem = f"> Este comando está em cooldown! Tente novamente em {dias} dias, {horas} horas, {minutos} minutos e {segundos} segundos."
			await ctx.send(mensagem, ephemeral=True)
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('> Você não tem permissão para usar esse comando!', ephemeral=True)
		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.send('> Eu não tenho permissão para executar esse comando!', ephemeral=True)
		else:
			data_options = JSONHandler.read_json('json_files/options.json')
			log_channel = ctx.guild.get_channel(data_options["bot_configs"]["channel_bot_erro"]) #Canal de logs de erros

			traceback_message = ''.join(traceback.format_exception(None, error, error.__traceback__))
			await log_channel.send(f'> **Unexpected error:**\n```\n{traceback_message}\n```')

bot = SupportBot(intents=intents, application_id=data_options["bot_configs"]["client_id"])

async def main():
	async with bot:
		await bot.start(TOKEN)

asyncio.run(main())
