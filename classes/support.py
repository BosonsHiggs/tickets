import json
from discord.ext import commands
from classes.dropdown import DropdownView
from classes.utilities import UniqueIdGenerator
from classes.io import JSONHandler
from classes.embeds import CustomEmbed

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='criar_ticket', brief="Cria um ticket")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def criar_ticket_command(self, ctx):
        unique_id = UniqueIdGenerator.generate_unique_custom_id()
        data_options = JSONHandler.read_json('json_files/options.json')
        options = data_options["options"]

        view = DropdownView(options, placeholder=data_options["channel_ticket"]["dropdown_placeholder"], custom_id_dropdown=f"dropdown_{ctx.message.id}", custom_id_button=unique_id)
        
        embed = (CustomEmbed(None, data_options["tickets"]["description"])
            .create_embed()
         )
        
        await ctx.send(embed=embed, view=view)

        # Save the ticket details in Redis when the ticket is created.
        ticket_details = {
            'user_id': ctx.author.id,
            'channel_id': ctx.channel.id,
            'button_id': unique_id,
            'dropdown_id': f"dropdown_{ctx.message.id}",
            "options": options
        }

        await self.bot.redis.set(f'ticket:{ctx.message.id}', json.dumps(ticket_details))
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Support(bot))
