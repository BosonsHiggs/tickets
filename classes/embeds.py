import discord

class CustomEmbed:
	""""
	TODO: Como usar:
	embed = (CustomEmbed("Title", "This is a description")
            .set_author("Author Name", icon_url="http://example.com/icon.png", url="http://example.com/")
            .set_footer("Footer text", icon_url="http://example.com/footer_icon.png")
            .set_thumbnail("http://example.com/thumbnail.png")
            .set_image("http://example.com/image.png")
            .add_field("Field 1", "Field 1 value")
            .add_field("Field 2", "Field 2 value", inline=True)
            .create_embed()
         )
	"""
	def __init__(self, title: str = None, description: str = None, color: discord.Color = discord.Color.blue()):
		self.title = title
		self.description = description
		self.color = color
		self.fields = []
		self.author = None
		self.footer = None
		self.thumbnail = None
		self.image = None

	def set_author(self, name: str, icon_url: str = None, url: str = None):
		self.author = {'name': name, 'icon_url': icon_url, 'url': url}
		return self

	def set_footer(self, text: str, icon_url: str = None):
		self.footer = {'text': text, 'icon_url': icon_url}
		return self

	def set_thumbnail(self, url: str):
		self.thumbnail = url
		return self

	def set_image(self, url: str):
		self.image = url
		return self

	def add_field(self, name: str, value: str, inline: bool = False):
		self.fields.append({'name': name, 'value': value, 'inline': inline})
		return self

	def create_embed(self):
		"""Create and return a discord.Embed instance."""
		embed = discord.Embed(
			title=self.title, 
			description=self.description, 
			color=self.color
		)

		if self.author:
			embed.set_author(name=self.author['name'], icon_url=self.author['icon_url'], url=self.author['url'])

		if self.footer:
			embed.set_footer(text=self.footer['text'], icon_url=self.footer['icon_url'])

		if self.thumbnail:
			embed.set_thumbnail(url=self.thumbnail)

		if self.image:
			embed.set_image(url=self.image)

		for field in self.fields:
			embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

		return embed
