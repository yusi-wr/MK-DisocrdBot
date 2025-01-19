from nextcord.ext import commands, tasks
import asyncio
from core import db
from core.events_q_cards import event_start, buttons
import time as pyTime

class QEvents(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot 
		self.started = False
		
	async def UpdateView(self):
		fetchAllData = db.events.find({})
		for data in fetchAllData:
			try:
				event_id = data["_id"]
				channel = await self.bot.fetch_channel(data["channel"])
				msg = await channel.fetch_message(event_id)
				time = data["start_time"]
				players = ["players"]
				role = channel.guild.get_role(data["role_id"])
				if data["started"] == "false":
					view = buttons.ViewEventEnter(role)
					view.Counter.label = str(len(players))
					await msg.edit(view=view)
				else:
					continue
			except:
				event_id = data["_id"]
				db.events.delete_one({"_id": event_id})
				continue
		
	@tasks.loop(seconds=3)
	async def TimeChecker(self):
		fetchAllData = db.events.find({})
		for data in fetchAllData:
			if data:
				try:
					event_id = data["_id"]
					channel = await self.bot.fetch_channel(data["channel"])
					msg = await channel.fetch_message(event_id)
					time = data["start_time"]
					role = channel.guild.get_role(data["role_id"])
					
					if data["started"] == "false":
						if pyTime.time() >= time:
							await msg.reply(f"{role.mention}\n- تبدء الفعالية بعد 30 ثانية", delete_after=30)
							await asyncio.sleep(30)
							await event_start(channel=channel, event_id=event_id)
							data["started"] = "true"
							db.events.update_one({"_id": event_id}, {"$set": {"started": data["started"]}})
							await msg.edit(view=None)
					else:
						continue
				except:
					pass
	
	@commands.Cog.listener()
	async def on_ready(self):
		await self.UpdateView()
		if not self.started:
			self.TimeChecker.start()
			self.started = True
			await asyncio.sleep(2)
			


def setup(bot):
	bot.add_cog(QEvents(bot))