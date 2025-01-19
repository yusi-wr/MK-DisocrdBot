from nextcord.ext import commands, tasks
from colorama import Fore
import asyncio
from deep_translator import GoogleTranslator
import feedparser
from Config import config
from core.helper import Helper

class UpdateCardsData(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot 
		self.started = False	
		
	@tasks.loop(hours=1)
	async def CarsUpdater(self):
		"""Tasks لتحديث نظام البطاقات"""
		await Helper.update_cards(bot=self.bot)
		
	@commands.Cog.listener()
	async def on_ready(self):
		if not self.started:
			self.CarsUpdater.start()
			self.started = True
			await asyncio.sleep(2)
			


def setup(bot):
	bot.add_cog(UpdateCardsData(bot))