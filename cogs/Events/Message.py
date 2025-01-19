from nextcord.ext import commands
from colorama import Fore
from core import Helper
from core.ui import menus
from core.embeds import embed_done, embed
from random import choice

class Message(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#for auto line
	@commands.Cog.listener("on_message")
	async def AutoLines(self, message):
		if message.author.bot:
			return
		try:
			guild = message.guild
			settings = Helper.guild_settings(guild)
			channel_list = settings["auto_line_channels"]
			if message.channel.id in channel_list:
				await Helper.send_image_lines(channel=message.channel, image="line.gif")
				return
		except:
			return
	
	#for message
	@commands.Cog.listener("on_message")
	async def Other(self, message):
		if message.author.bot:
			return
		try:
			if (message.content == "السلام عليكم" or message.content == "سلام عليكم" or message.content == "السلام عليكم ورحمة الله" or message.content == "سلام عليكم ورحمة الله"):
				await message.reply(choice(["وعليكم السلام ورحمة الله", "وعليكم السلام ورحمة الله وبركاته", "وعليكم السلام بارك الله فيك"]))
				return
			if (message.content.lower() == "p"):
				em = Helper.get_user_profile(user=message.author)
				await message.reply(embed=em)
			if (message.content == f"{self.bot.user.mention}"):
				await message.reply(embed=embed(user=message.guild.me, desc="# Prefix commands\n- #help\n- #help command name\n# Slash commands\n- /cards\n- /duels\n- /set\n- /store\n- /items\n- /send\n- /profile", icon_url="", title="**• بعض المساعدة؟ •**"), view=menus.GuideMenuSelect(message.author))
				return
			if (message.content == "خط"):
				if Helper.check_its_admin(message.author):
					await Helper.send_image_lines(message.channel, "line.gif")
					await message.delete()
					return
				else:
					return
		except:
			return
	
def setup(bot):
	bot.add_cog(Message(bot))