from nextcord.ui import Button, button, View
from nextcord import ButtonStyle, Interaction
from Config import emojis
from core import db
from core.embeds import embed
import asyncio


#Class for create buttons
class CreateButton(Button):
	def __init__(self, event_id,  name, correct):
		super().__init__(label=name, style=ButtonStyle.gray, emoji=emojis["card"])
		
		self.event_id = event_id
		self.correct = correct
		self.name = name
		
	async def callback(self, interaction: Interaction):
		from core.events_q_cards import check_event_round, end_event, event_start
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		data = db.events.find_one({"_id": self.event_id})
		
		main_message = await interaction.channel.fetch_message(self.event_id)
		role = interaction.guild.get_role(data["role_id"])
		
		if not user.id in data['players']:
			await interaction.followup.send("**يبدو انك لم تشارك في الفعالية لذا لا يمكنك الاجابة**", ephemeral=True)
			return
		
		if self.name == self.correct:
			self.view.on_timeout = None
			points = 1	
			await interaction.message.reply(f"{user.mention} احصنت", embed=embed(user=interaction.guild.me, desc=f"الإجابة الصحيحة هي: {self.correct}\n- {points} نقطة لك"), delete_after=15)
			await interaction.message.delete()
			
			if str(user.id) in data["stats"]:
				data["stats"][str(user.id)]["points"] += points
			else:
				data["stats"][str(user.id)] = {}
				data["stats"][str(user.id)]["points"] = points
				data["stats"][str(user.id)]["user"] = user.mention
			
			data["round"] += 1
			data = db.events.update_one({"_id": self.event_id}, {"$set": data})
		
			send = await main_message.reply(embed=embed(user=interaction.guild.me, desc="جاري بدا الجولة التالية بعد 10 ثانية كونوا مستعدين"))
			await asyncio.sleep(12)
			if check_event_round(self.event_id):
				await send.edit(embed=embed(user=interaction.guild.me, desc="يبدوا ان هذه كانت الجولة الأخير معنا اليوم ^_^ \n- 15 ثانية ويتم اعلان التائج"))
				await asyncio.sleep(10)
				await end_event(self.event_id, interaction.channel)
			else:
				await event_start(self.event_id, interaction.channel)
			await send.delete()
		else:
			await interaction.followup.send("**مع الأسف اجابة خاطأة حاول مجددا بسرعة قبل ان يفوز احد**", ephemeral=True)


class ViewQEvent(View):
	def __init__(self, event_id, names: list, correct: str):
		super().__init__(timeout=None)
		self.names = sorted(names)
		self.correct = correct
		self.event_id = event_id
		self.msg = None
		
		for name in self.names:
			self.add_item(CreateButton(event_id=event_id, name=name, correct=correct))
		

class ViewEventEnter(View):
	def __init__(self, role):
		super().__init__(timeout=None)
		self.role = role
	
	@button(label="مشاركة", style=ButtonStyle.gray, emoji=emojis["members"], custom_id="enter-event")
	async def enter_event(self, button:  Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		_id = interaction.message.id
		user = interaction.user
		data = db.events.find_one({"_id":_id})
		
		if user.id in data["players"]:
			await interaction.followup.send("**انت بالفعل مشارك في الفعالية!**", ephemeral=True)
			return
			
		data["players"].append(user.id)
		db.events.update_one({"_id": _id}, {"$set": {"players":data["players"]}})
		self.Counter.label = str(len(data["players"]))
		await user.add_roles(self.role)
		await interaction.followup.send("**تم تسجيلك في الفعالية بنجاح شكرا**", ephemeral=True)
		await interaction.message.edit(view=self)
	
	@button(label="0", style=ButtonStyle.gray, emoji=emojis["members"], disabled=True)
	async def Counter(self, button: Button, interaction: Interaction):
		pass
		