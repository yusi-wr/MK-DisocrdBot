from nextcord.ext import commands, tasks
from core import db, embeds
from Config import config, emojis
import time as pyTime
import random
import asyncio
from core import Helper
from core.ui.buttons import GiveawayButton, DailyGiftsButton

class GiveawayHanding(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.is_started = False
	
	def Deleter(self, message):
		db.giveaway.delete_one({"_id":message.id})
		
	async def ViewUpdater(self):
		fetch_all = db.giveaway.find({})
		for data in fetch_all:
			if data:
				try:
					channel = await self.bot.fetch_channel(data["channel"])
					message = await channel.fetch_message(data["_id"])
					time = data["time"]
					participants = data["participants"]
					view=GiveawayButton(time=time - pyTime.time())
					view.Counter.label = str(len(participants))
					await message.edit(view=view)
					view.message = message
				except:
					db.giveaway.delete_one({"_id":data["_id"]})
				
	@tasks.loop(seconds=2)
	async def Handler(self):
		fetch_all = db.giveaway.find({})
		for data in fetch_all:
			try:
				channel = await self.bot.fetch_channel(data["channel"])
				message = await channel.fetch_message(data["_id"])
				hoster = await self.bot.fetch_user(data["hoster"])
				prize = data["prize"]
				time = data["time"]
				winners_count = data["winners"]
				participants = data["participants"]
				guild = channel.guild
				if pyTime.time() >= time:
					 joins = []
					 for user_id in participants:
					 	user = await self.bot.fetch_user(user_id)
					 	if user is not None:
					 		joins.append(user.mention)
					 if len(joins) > 0:
					 	if len(joins) <= winners_count:
					 		winners = random.sample(joins, len(joins))
					 	else:
					 		winners = random.sample(joins, winners_count)
					 	em = embeds.embed(user=hoster, title=f"**{prize}**", desc=f"\n- {emojis['time']} اتهتي منذ: <t:{int(time)}:R>\n- {emojis['author']} تم بواسطة: {hoster.mention}",icon_url="https://cdn.discordapp.com/emojis/747504960517963957.png")
					 	text  = f"- {hoster.mention}\n- انهى وقت الجيف ومبروك للفائز معانا 🥳\n" + ", ".join(x for x in winners)
					 	await message.edit(embed=em)
					 	await message.reply(f">>> **{text}**")
					 	self.Deleter(message)
					 else:
					 	em = embeds.embed(user=hoster, title=f"**{prize}**", desc=f"\n- {emojis['time']} اتهتي منذ: <t:{int(time)}:R>\n- {emojis['author']} تم بواسطة: {hoster.mention}",icon_url="https://cdn.discordapp.com/emojis/747504960517963957.png")
					 	text  = f"- {hoster.mention}\n- الجيف خلص بس مفيش فائزين" 
					 	await message.edit(embed=em)
					 	await message.reply(f">>> **{text}**")
					 	self.Deleter(message)
			except Exception as E:
						pass
						
	@tasks.loop(minutes=30)
	async def DailyGifts(self):
		user = self.bot.user
		if Helper.check_cooldwon(user=user, cmd="dailygift", type=24):
			channel = await self.bot.fetch_channel(1265436181387022358)
			
			text = "مرحبا بجميع الاعبين الأبطال صندوق الهداية اليومي مفتوح وجاهز للإستلام أسرع واحد يأخذ الصندوق هو المحظوظ للحصول على ما يقارب 10000$ فضة او 50 نقطة مبارزة\n- ياترى من المحظوظ اليوم ؟\n- لا تنسى #daily للمزيد"
			em = embeds.embed(user=user, desc=text, icon_url="https://cdn.discordapp.com/emojis/1094875501614600233.png")
			
			try:
				await channel.send("• @here •", embed=em, view=DailyGiftsButton())
			except:
				return
		else:
			return
	
	@commands.Cog.listener()
	async def on_ready(self):
		if not self.is_started:
			self.Handler.start()
			self.is_started = True
			await asyncio.sleep(2)
			self.DailyGifts.start()
			await asyncio.sleep(2)
		await self.ViewUpdater()
	
		
def setup(bot):
	bot.add_cog(GiveawayHanding(bot))