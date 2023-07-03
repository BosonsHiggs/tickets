import json
import discord
import traceback
from discord.ext import commands
from classes.dropdown import DropdownView
from classes.buttons import DelButton, DeleteButtonView
from classes.io import JSONHandler
from typing import Optional, Literal
from discord import app_commands

data_handler = JSONHandler.read_json('json_files/options.json')

MY_GUILD_ID = discord.Object(data_handler["bot_configs"]["sync_guild_id"], type=discord.Guild)

class Creator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.hybrid_command(name='sync', brief="sincronizar comandos")
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	@app_commands.guilds(MY_GUILD_ID)
	async def sync_command(
		self, 
		ctx: commands.Context, 
		guilds: Optional[str] = None,
		spec: Optional[Literal[
							   "Clear and local sync",
							   "Clear local slash",
							   "Clear local message context",
							   "Clear local user context",
							   "Clear global slash",
							   "Clear global message context",
							   "Clear global user context",
							   "Global sync",
							   "Copy global to local",
							   "Local sync"
							  ]
					  ] = None
	) -> None:
		assert ctx.guild is not None
		await ctx.defer(ephemeral=True)

		msg = await ctx.send("Wait!")

		##Guilds
		try:
			next_word = guilds.split(';', maxsplit=1)[-1].split(maxsplit=1)[0]
			next_word = next_word.replace(" ", "")

			if (next_word != guilds) and ( ';' not in guilds):
				await msg.edit(content=f'> *As IDs dos servidores devem ser sepradas por ponto e vírgula!* 😪')
				return

			guilds = guilds.replace(" ", "").split(';')

			guilds = (discord.Object(id) for id in guilds)
		except:
			guilds = None
		#End guilds


		if guilds is None:
			guilds = ctx.guild
			if spec is not None:
				if spec.lower() == "clear and local sync":
					self.bot.tree.clear_commands(guild=guilds)
					await self.bot.tree.sync(guild=guilds)
				elif spec.lower() == "local sync":
					await self.bot.tree.sync(guild=guilds)
				elif spec.lower() == "copy global to local":
					self.bot.tree.copy_global_to(guild=guilds)
					await self.bot.tree.sync(guild=guilds)
				elif spec.lower() == "clear local slash":
					self.bot.tree.clear_commands(guild=guilds, type=discord.AppCommandType.chat_input)
					await self.bot.tree.sync(guild=guilds)
				elif spec.lower() == "clear local message context":
					self.bot.tree.clear_commands(guild=guilds, type=discord.AppCommandType.message)
					await self.bot.tree.sync(guild=guilds)
				elif spec.lower() == "clear local user context":
					self.bot.tree.clear_commands(guild=guilds, type=discord.AppCommandType.user)
					await self.bot.tree.sync(guild=guilds)
				elif spec.lower() == "clear global slash":
					self.bot.tree.clear_commands(guild=None, type=discord.AppCommandType.chat_input)
					await self.bot.tree.sync()
				elif spec.lower() == "clear global message context":
					self.bot.tree.clear_commands(guild=None, type=discord.AppCommandType.message)
					await self.bot.tree.sync()
				elif spec.lower() == "clear global user context":
					self.bot.tree.clear_commands(guild=None, type=discord.AppCommandType.user)
					await self.bot.tree.sync()
				elif spec.lower() == "global sync":
					await self.bot.tree.sync()
				
			await msg.edit(
				content=f"Comandos sincronizados {'globalmente!' if spec is None else 'com o servidor local!'}"
			)
			return
			

		fmt = 0
		for guild in guilds:
			try:
				await self.bot.tree.sync(guild=guild)
			except discord.HTTPException:
				pass
			else:
				fmt += 1

		await msg.edit(content=f"Sincronizado com o(s) servidor{'es'[:fmt^1]}.")

	@commands.hybrid_command(name='del_key_redis', brief="Deletar uma chave do servidor Redis")
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	@app_commands.guilds(MY_GUILD_ID)
	async def del_key_redis_command(self, ctx, key: str):
		await self.bot.redis.delete(key)
		await ctx.send(f"A chave {key} foi deletada com sucesso!")

	@commands.hybrid_command(name='clear_all_redis', brief="Apaga o banco de dados atual do servidor Redis")
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	@app_commands.guilds(MY_GUILD_ID)
	async def clear_all_redis_command(self, ctx):
		await self.bot.redis.flushdb() #apaga o banco de dados atual ou self.bot.redis.flushall() para pagar todos
		await ctx.send(f"O banco de dados foi resetado!")

	@commands.hybrid_command(name='load_buttons', brief="Ler todos os botões e dropdowns após o reinicio do bot")
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	@app_commands.guilds(MY_GUILD_ID)
	async def load_buttons_command(self, ctx):
		if not hasattr(self.bot, "persistent_views_added"):
			self.bot.persistent_views_added = True

		options = data_handler["options"]

		async def load_buttons_dropdowns():
			keys = await self.bot.redis.keys('ticket:*')
			for key in keys:
				ticket_details = json.loads(await self.bot.redis.get(key))

				#Del buttons
				del_button = DelButton(discord.ButtonStyle.danger, '🗑️', str(ticket_details["button_id"]))
				delete_button = DeleteButtonView(del_button)
				#Dropdown
				dropdown_view = DropdownView(options, placeholder=data_handler["channel_ticket"]["dropdown_placeholder"], custom_id_dropdown=str(ticket_details["dropdown_id"]), custom_id_button=str(ticket_details["button_id"]))

				# Add del_button to the view
				#dropdown_view.add_item(del_button)

				# Add the view to the bot
				self.bot.add_view(dropdown_view)
				self.bot.add_view(delete_button)

		await load_buttons_dropdowns()
		await ctx.send("Botões e dropdowns restaurados com sucesso!")
		"""except Exception as e:
			print(f"An error occurred: {e}")
			tb = traceback.format_exc()
			print(tb)"""
		
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Creator(bot), guild=MY_GUILD_ID)
