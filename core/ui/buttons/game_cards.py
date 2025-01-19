from nextcord import Interaction, ButtonStyle, Message
from nextcord.ui import Button, button, View
from Config import config, emojis
from random import choice, randint
from core import db, embeds, cards
import asyncio

#Save points
async def PointsClim(user, points):
	update = {
	  "$inc": {"coins": points}
	}
	db.users.update_one({"_id": user.id}, update)

#Class button game
class GameButton(Button):
	def __init__(self, correct_name, name, origin_inter, points, round, CountAnswer, fromArchetype):
		super().__init__(label=name, style=ButtonStyle.gray, emoji=emojis["card"])
		self.correct_name = correct_name
		self.origin_inter = origin_inter
		self.CountAnswer = CountAnswer
		self.points = points
		self.round = round
		self.from_archetype = fromArchetype
		
	async def Restart(self):
		await cards.CardsGame(interaction=self.origin_inter, points=self.points, round=self.round, CountAnswer=self.CountAnswer, archetype=self.from_archetype)
		
	async def callback(self, interaction: Interaction):
		user = interaction.user
		await interaction.response.defer(ephemeral=True)
		
		if user.id != self.origin_inter.user.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
		
		if self.label == self.correct_name:
			self.points += randint(100, 200)
			self.CountAnswer += 1
			self.round += 1
			
			await interaction.followup.send(embed=embeds.embed(user=user,desc="أحسنت إجابتك صحيحة رائع جدا ", icon_url="https://cdn.discordapp.com/emojis/803747754923786300.png"), delete_after=8)
			self.style = ButtonStyle.green
			await self.view.Disabled()
			await asyncio.sleep(4)
			await interaction.message.delete()
			await self.Restart()
		else:
			self.round += 1
			
			await interaction.followup.send(embed=embeds.embed(user=user,desc=f"إجابة خطأة للأسف\n- الاجابة كانت: {self.correct_name}", icon_url="https://cdn.discordapp.com/emojis/803747126752444487.png"), delete_after=12)
			self.style = ButtonStyle.red
			for btn in self.view.children:
				if btn.label == self.correct_name:
					btn.style = ButtonStyle.green
			await self.view.Disabled()
			await asyncio.sleep(4)
			await interaction.message.delete()
			await self.Restart()

#Class game view
class CardsGameButton(View):
	def __init__(self, origin_inter: Interaction, names: list, CountAnswer: int, points: int, round: int, correct_name,fromArchetype):
		super().__init__(timeout=30)
		self.origin_inter = origin_inter
		self.points  = points
		self.from_archetype = fromArchetype
		self.message = None
		self.stoped = False
		self.correct_name  = correct_name
		
		for name in sorted(names):
			name=choice(names)
			names.remove(name)
			self.add_item(GameButton(origin_inter=origin_inter, correct_name=correct_name, name=name, points=points, round=round, CountAnswer=CountAnswer, fromArchetype=self.from_archetype))
	
	async def Disabled(self, by_time = False):
		for btn in self.children:
			btn.disabled = True
			if by_time:
				if btn.label == self.correct_name:
					btn.style = ButtonStyle.green
				else:
					btn.style = ButtonStyle.red
			await self.message.edit(view=self)
			
	async def on_timeout(self):
		user = self.origin_inter.user
		try:
			if not self.stoped:
				await self.Disabled(by_time=True)
				await self.message.reply(embed=embeds.embed(user=user, desc=f"لقد انتهى الوقت. وتم الخروج واغلاق اللعبة\n- لقد جمعت: {self.points:,}$ فضة\n- الاجابة الصحيحة لهذه الجولة كانت\n- {self.correct_name}", icon_url="https://cdn.discordapp.com/emojis/1029866581993476200.png"))
			else:
				await self.Disabled()
			if self.points > 0:
				await PointsClim(self.origin_inter.user, self.points)
		except:
				pass
	
	#Button quit form the game
	@button(label="خروج", style=ButtonStyle.red, emoji=emojis["cancel"])
	async def QuitGame(self, button: Button, interaction: Interaction):
		user = interaction.user
		await interaction.response.defer(ephemeral=True)
		
		if user.id != self.origin_inter.user.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
		
		self.stoped = True
		await self.on_timeout()
		await interaction.followup.send(embed=embeds.embed(user=user, desc=f"**تم إيقاف والخروج من اللعبة\n- لقد جمعت: {self.points:,}$ فضة\n- الاجابة الصحيحة لهذه الجولة كانت\n- {self.correct_name}**", icon_url="https://cdn.discordapp.com/emojis/818221243471364226.png"))

