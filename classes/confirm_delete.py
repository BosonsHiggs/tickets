import discord
from classes.io import JSONHandler

class ConfirmDelete(discord.ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(timeout=None)
		self.message = None

	@discord.ui.button(label="Sim", style=discord.ButtonStyle.green, custom_id="sim:button")
	async def confirm(self,  interaction: discord.Interaction, button: discord.ui.Button):
		# Se o membro confirmar a deleção, então envie uma mensagem ao canal de logs
		data_options = JSONHandler.read_json('json_files/options.json')

		self.message = interaction.message or None
		log_channel = interaction.guild.get_channel(data_options["bot_configs"]["channel_ticket_log"]) #Canal de logs
		msg_log = data_options["channel_ticket"]["message_channel_deleted"]
		
		await log_channel.send(f"{msg_log}".format(interaction.user, interaction.user.id, interaction.channel.name))
		await interaction.channel.delete()

	@discord.ui.button(label="Não", style=discord.ButtonStyle.red, custom_id="nao:button")
	async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.message = interaction.message or None
		try:
			await interaction.message.delete()
		except:
			data_options = JSONHandler.read_json('json_files/options.json')
			msg_delete = data_options["channel_ticket"]["ephemeral_message"].format(interaction.user.mention)
			await interaction.edit_original_response(msg_delete, view=ConfirmDelete(), ephemeral=True)


	async def on_timeout(self):
		if hasattr(self, "message"):
			if self.message is None: return
		else:
			return None

		if self.message is None: return
		if self.message:  # Verificar se a mensagem original foi armazenada
			await self.message.delete()  # Deletar a mensagem original