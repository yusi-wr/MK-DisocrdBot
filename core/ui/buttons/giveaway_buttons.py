from nextcord import Interaction, ButtonStyle
from nextcord.ui import View, button, Button
from Config import emojis, images
from core import db
from random import choice, randint
from core.embeds import embed

class DailyGiftsButton(View):
	def __init__(self):
		super().__init__(timeout=None)
		
	@button(label="استلام", style=ButtonStyle.green, emoji=emojis["box"])
	async def Gifts(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		gift_type = choice(["coins", "points"])
		text = f"- استلم {user.mention} الصندوق اليومي اليوم مبروك لك"
		if gift_type == "coins":
			gift = randint(4000, 10000)
			text += f"\n- لقد حصلت: {emojis['coins']} {gift:,}$ فضة"
			db.users.update_one({"_id": user.id}, {"$inc":{"coins": gift}})
		else:
			gift = randint(20, 50)
			text += f"\n- لقد حصلت: {emojis['points']} {gift} نقطة مبارزة"
			db.users.update_one({"_id": user.id}, {"$inc":{"points": gift}})
		
		text += "\n- لا تنسو اللعب المباريات بالنظام لتزويد المتعة اللعب والتحديات وربح المزيد من الناقط والفضة ورفع مستوى الرنك \n- لإنشاء مباريات واللعب↓"
		text += "\n- /duels create | لإنشاء\n- /duels accept | تأكيد المباراة\n- /duels show | اظهار قائمة المباريات"
		text += "\n- للمزيد من التفاصيل منشن البوت"
		em = embed(user=user, desc=text, icon_url="https://cdn.discordapp.com/emojis/1094875501614600233.png",image_url=images["bg"])
		button.disabled = True
		button.label = "تم اتسلام..."
		await interaction.message.edit(embed=em, view=self)


class GiveawayButton(View):
	def __init__(self, time):
		super().__init__(timeout=time)
		
		self.message = None
		
	async def on_timeout(self):
		for b in self.children:
			b.disabled = True
		await self.message.edit(view=self)
		
	@button(label="مشاركة", style=ButtonStyle.green, emoji=emojis["giveaway"], custom_id="joingive")
	async def GiveawayJoin(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		data = db.giveaway.find_one({"_id":self.message.id})
		if not data:
			await interaction.followup.send("لم يعد من  الممكن المشاركة في الجيف  آسف", ephemeral=True)
			return
		
		participants = data["participants"]
		if user.id in participants:
			await interaction.followup.send("انت بالفعل مشارك في الجيف ", ephemeral=True)
		else:
			participants.append(user.id)
			update ={
				"$set": {"participants":participants}
			}
			db.giveaway.update_one({"_id":self.message.id}, update)
			await interaction.followup.send("تم  بنجاح اصبحت في قائمة المشاركين في الجيف ", ephemeral=True)
			self.Counter.label = str(len(participants))
			await interaction.message.edit(view=self)
	
	@button(label="0", style=ButtonStyle.gray, emoji=emojis["members"], custom_id="Counter", disabled=True)
	async def Counter(self, button: Button, interaction: Interaction):
		pass