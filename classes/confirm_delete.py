import discord
from classes.io import JSONHandler

class ConfirmDelete(discord.ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(timeout=None) # View will stop listening for interaction after 60 seconds.
		self.message = None

	@discord.ui.button(label="Sim", style=discord.ButtonStyle.green, custom_id="sim:button")
	async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
		# Se o membro confirmar a deleção, então envie uma mensagem ao canal de logs
		data_options = JSONHandler.read_json('json_files/options.json')

		self.message = button.message
		log_channel = button.guild.get_channel(data_options["bot_configs"]["channel_ticket_log"]) #Canal de logs
		msg_log = data_options["channel_ticket"]["message_channel_deleted"]
		
		await log_channel.send(f"{msg_log}".format(button.user, button.user.id, button.channel.name))
		await button.channel.delete()

	@discord.ui.button(label="Não", style=discord.ButtonStyle.red, custom_id="nao:button")
	async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
		self.message = button.message
		await button.message.delete()

	async def on_timeout(self):
		if hasattr(self, "message"):
			if self.message is None: return
		else:
			return None

		if self.message:  # Verificar se a mensagem original foi armazenada
			await self.message.delete()  # Deletar a mensagem original