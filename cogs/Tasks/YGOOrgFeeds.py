from nextcord.ext import commands, tasks
from colorama import Fore
import asyncio
from deep_translator import GoogleTranslator
import feedparser
from Config import config
from core.helper import Helper
import json

class News(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot 
		self.started = False
		
	@tasks.loop(hours=1)
	async def NewsUpdate(self):
		url = "https://ygorganization.com/feed/"
		try:
			with open("./data/ygo_feed_news.json", "r") as f:
				data = json.load(f)
		except:
			data = {
				"now_feed_url": ""
			}
			
		for guild in self.bot.guilds:
			
			settings = Helper.guild_settings(guild)
			if settings["channel_news"]:
				channel = await self.bot.fetch_channel(settings["channel_news"])
					
				parser = feedparser.parse(url)
				feed = parser.entries[0]
				try:
					text_ar = GoogleTranslator(source="auto", target="ar").translate(feed.summary)
					message = f">>> **{feed.title}\n```{feed.summary}```\n```{text_ar}```\n{feed.link} **"
					if data["now_feed_url"] == feed.link:
								return
					send = await channel.send(message)
					await send.edit(message + "\n- @here")
					data["now_feed_url"] = feed.link
					with open("./data/ygo_feed_news.json", "w") as f:
						json.dump(data, f, indent=2)
				except:
					return
		
	@commands.Cog.listener()
	async def on_ready(self):
		if not self.started:
			self.NewsUpdate.start()
			self.started = True
			await asyncio.sleep(2)
			


def setup(bot):
	bot.add_cog(News(bot))