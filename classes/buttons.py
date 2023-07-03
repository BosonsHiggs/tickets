import discord
import traceback
from classes.confirm_delete import ConfirmDelete
from classes.io import JSONHandler

class DeleteButtonView(discord.ui.View):
	def __init__(self, button: discord.ui.Button):
		super().__init__(timeout=None)
		self.add_item(button)

class DelButton(discord.ui.Button):
	def __init__(self, style, emoji, custom_id):
		super().__init__(style=style, emoji=emoji, custom_id=custom_id)

	async def callback(self, interaction: discord.Interaction):
		await self.delete_ticket(interaction)

	async def delete_ticket(self, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True)
		channel = interaction.channel

		data_options = JSONHandler.read_json('json_files/options.json')
		try:
			msg_delete = data_options["channel_ticket"]["messge_ticket_deleted_press"].format(interaction.user.mention)
			await channel.send(msg_delete, view=ConfirmDelete())
		except Exception as e:
			print(f"An error occurred: {e}")
			tb = traceback.format_exc()
			print(tb)
