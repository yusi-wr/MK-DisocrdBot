import nextcord
from nextcord.ext import commands, tasks
import asyncio
from random import choice
from core import items, Helper, db, stores
from core.embeds import embed

class ItemsTimeChecker(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.is_started = False
		
	#--------------(Tasks)-------------
	#tasks time items checker
	@tasks.loop(seconds=5)
	async def ActiviteChecker(self):
		"""لا تحذف ولا تغيير حاجة الا لو كنت تعرف تعمل ايه"""
		d = db.users.find({})
		for userdata in d:
			user = await self.bot.fetch_user(userdata["_id"])
			activite = userdata["activite"].copy()
			if len(activite) == 0:
				continue
			for i, val in activite.items():
				if Helper.CheckItemsTime(val["date"], val["type"]):
					del userdata["activite"][i]
					item = stores.items[i]
					#print(" • Done 1 •")
					try:
						await user.send(f"- **السلام عليكم {user.mention}**", embed=embed(user=self.bot.user, desc=f"لقد انتهي تأثير `{item['name']}` لتتمكن من الاستفادة منه من جديد إستخدم الأمر التالي\n```/items use```", title=f"** • {item['name']} • **", icon_url=item["icon"], image_url="https://cdn.discordapp.com/attachments/1249128052856721510/1303840664232132681/1730930147305.jpg"))
					except:
						pass
					db.users.update_one({"_id": user.id}, {"$set":{"activite": userdata["activite"]}})
					#print(" • Done •")
					#print(db.users.find_one({"_id": user.id}))
		
		
	@commands.Cog.listener()
	async def on_ready(self):
		"""on_ready  event"""
		if not self.is_started:
			self.ActiviteChecker.start()
			self.is_started = True
			await asyncio.sleep(2)
		
		
def setup(bot):
	bot.add_cog(ItemsTimeChecker(bot))
