import nextcord
from nextcord.ext import commands
from colorama import Fore
from core.ui.buttons import ButtonSuggestion

class Ready(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="#help • /duels"))
		print(f"{Fore.LIGHTMAGENTA_EX} • Bot status is: {Fore.LIGHTGREEN_EX}{self.bot.status}{Fore.RESET}")
		
		
		
def setup(bot):
	bot.add_cog(Ready(bot))