from nextcord.ext import commands
from colorama import Fore
from core import Helper, db
from core.embeds import embed_done, embed
from core.ui.buttons import ButtonSuggestion
from random import choice
from datetime import datetime

class Suggestion(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	async def updater_views(self):
		fetch_all = db.suggetions.find({})
		try:
			for data in fetch_all:
				guild = self.bot.get_guild(data["guild_id"])
				settings = Helper.guild_settings(guild)
				sug_channel = guild.get_channel(settings["suggestion_channel"])
				msg = await sug_channel.fetch_message(data["_id"])
				view =  ButtonSuggestion()
				view.Up.label = str(len(data["up"]))
				view.Dwon.label = str(len(data["dwon"]))
				
				await msg.edit(view=view)
		except:
			return
			
	@commands.Cog.listener()
	async def on_ready(self):
		await self.updater_views()
	
	#for suggestion
	@commands.Cog.listener("on_message")
	async def suggestion(self, message):
		"""ايفنت يحندل الإقتراحات"""
		if message.author.bot:
			return
		try:
			guild = message.guild
			author = message.author
			settings = Helper.guild_settings(guild)
			sug_channel = guild.get_channel(settings["suggestion_channel"])
			if not sug_channel:
				return
			if message.channel.id != sug_channel.id:
				return
			
			await Helper.send_image_lines(sug_channel, "line.gif")
			sug = await sug_channel.send(embed=embed(user=author, desc=message.content + f"\n- تم بواسطة: {author.mention}", icon_url="https://cdn.discordapp.com/emojis/979042704195457064.png"), view=ButtonSuggestion())
			await Helper.send_image_lines(sug_channel, "line.gif")
			await sug.edit(content="@here")
			await message.delete()
			
			data = {
				"_id": sug.id,
				"guild_id": guild.id,
				"up": [],
				"dwon": [],
				"date": str(datetime.utcnow())
			}
			db.suggetions.insert_one(data)
		except:
			return 
		
		
		
def setup(bot):
	bot.add_cog(Suggestion(bot))