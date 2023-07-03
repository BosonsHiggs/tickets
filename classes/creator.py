import json
import discord
import traceback
from discord.ext import commands
from classes.dropdown import DropdownView
from classes.buttons import DelButton, DeleteButtonView
from classes.io import JSONHandler

class Creator(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	async def del_key_redis(self, ctx, key: str):
		await self.bot.redis.delete(key)
		await ctx.send(f"A chave {key} foi deletada com sucesso!")

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	async def clear_all_redis(self, ctx):
		await self.bot.redis.flushdb() #apaga o banco de dados atual ou self.bot.redis.flushall() para pagar todos
		await ctx.send(f"O banco de dados foi resetado!")

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.is_owner()
	async def load_buttons(self, ctx):
		if not hasattr(self.bot, "persistent_views_added"):
			self.bot.persistent_views_added = True

		data = JSONHandler.read_json('json_files/options.json')
		options = data["options"]

		async def load_buttons_dropdowns():
			keys = await self.bot.redis.keys('ticket:*')
			for key in keys:
				ticket_details = json.loads(await self.bot.redis.get(key))

				#Del buttons
				del_button = DelButton(discord.ButtonStyle.danger, '🗑️', str(ticket_details["button_id"]))
				delete_button = DeleteButtonView(del_button)
				#Dropdown
				dropdown_view = DropdownView(options, response="You selected:", placeholder="Choose a support category", custom_id_dropdown=str(ticket_details["dropdown_id"]), custom_id_button=str(ticket_details["button_id"]))

				# Add del_button to the view
				#dropdown_view.add_item(del_button)

				# Add the view to the bot
				self.bot.add_view(dropdown_view)
				self.bot.add_view(delete_button)
		try:
			await load_buttons_dropdowns()
		except Exception as e:
			print(f"An error occurred: {e}")
			tb = traceback.format_exc()
			print(tb)
		
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Creator(bot))
