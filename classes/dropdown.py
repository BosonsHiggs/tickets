import discord
from classes.buttons import DelButton, DeleteButtonView
from classes.embeds import CustomEmbed
from classes.io import JSONHandler

class Dropdown(discord.ui.Select):
	def __init__(self, args, **kwargs):
		placeholder = kwargs.get('placeholder') or "You didn't type the placeholder"
		min_values = kwargs.get('min_values') or 1
		max_values = kwargs.get('max_values') or 1
		
		self.custom_id_dropdown =  kwargs.get("custom_id_dropdown") or None
		self.custom_id_button = kwargs.get("custom_id_button") or None
		self.data_options = JSONHandler.read_json('json_files/options.json')
		
		# Defina as opções que serão apresentadas dentro do menu suspenso.

		options = [
			discord.SelectOption(label=x, description=y, emoji=z) for (x, y, z) in args
		]

		self.labels = [x for (x, y, z) in args ]

		# O espaço reservado (placeholder) é o que será mostrado quando nenhuma opção for escolhida
		# Os valores mínimos e máximos indicam que só podemos escolher uma das três opções
		# O parâmetro opções define as opções do menu suspenso. Nós definimos isso acima
		super().__init__(
						 placeholder=placeholder, 
						 min_values=min_values, 
						 max_values=max_values, 
						 options=options,
						 custom_id=self.custom_id_dropdown 
						 )

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True)
		assert self.view is not None
		view: DropdownView = self.view

		view.value = self.labels.index(self.values[0])
		view.interaction = interaction

		#Pegar o item clicado
		selected_category = self.values[0]

		guild = interaction.guild
		
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			interaction.user: discord.PermissionOverwrite(read_messages=True)
		}

		# Verificar se já existe a categoria
		category = discord.utils.get(guild.categories, name=selected_category)
		if category is None:
			category = await guild.create_category(name=selected_category)

		#Nome do canal a ser criado
		channel_name = f'{selected_category}-{interaction.user.id}'.replace(' ', '-').lower()

		# Verificar se o canal já existe
		existing_channel = discord.utils.get(guild.text_channels, name=channel_name, category=category)
		if existing_channel:
			if existing_channel.permissions_for(interaction.user).read_messages:
				await interaction.followup.send(self.data_options["channel_ticket"]["message_channel_exist"], ephemeral=True)
				return

		#Canal do ticket
		channel = await guild.create_text_channel(name=f'{selected_category}-{interaction.user.id}', category=category, overwrites=overwrites)

		#Mensagem de resposta
		channel_id = interaction.channel.id
		await interaction.followup.send(self.data_options["channel_ticket"]["message_ticket_created"].format(channel_id), ephemeral=True)

		#Botão para deletar o ticket
		del_button = DelButton(discord.ButtonStyle.danger, '🗑️', self.custom_id_button)
		delete_button = DeleteButtonView(del_button)
		
		# Nossa embed personalizada
		embed = (CustomEmbed(None, self.data_options["channel_ticket"]["message_ticket"].format(interaction.user.mention))
            .create_embed()
         )
		
		#enviar mensagem ao canal de tickets
		await channel.send(embed=embed, view=delete_button)


class DropdownView(discord.ui.View):
	def __init__(self, args, **kwargs):
		super().__init__(timeout=None)
		response = kwargs.get('response')
		placeholder = kwargs.get('placeholder') or "You didn't type the placeholder"
		min_values = kwargs.get('min_values') or 1
		max_values = kwargs.get('max_values') or 1
		
		self.custom_id_dropdown =  kwargs.get('custom_id_dropdown')
		self.custom_id_button = kwargs.get("custom_id_button")

		# Adiciona o SelectMenu/ Dropdown ao nosso objeto view.
		self.add_item(Dropdown(args, placeholder=placeholder, min_values=min_values, max_values=max_values, custom_id_dropdown=self.custom_id_dropdown, custom_id_button=self.custom_id_button))