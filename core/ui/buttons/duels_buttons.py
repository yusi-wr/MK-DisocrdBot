from nextcord import Interaction, ButtonStyle, Member
from nextcord.ui import Button, button, View
from Config import emojis
from core.embeds import embed, embed_done, embed_errors
from core import db, helper

class DuelButtonDelete(Button):
	def __init__(self, author: Member = None, match_id: int = None):
		super().__init__(label="حذف المباراة", style=ButtonStyle.danger, emoji=emojis["delete"])
		self.match_id = match_id
		self.author = author
		
	async def callback(self, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user_inter = interaction.user
		if self.author is None:
			self.author = self.view.author
		if self.match_id is None:
			self.match_id = self.view.names[self.view.page - 1]
		
		if user_inter.id != self.author.id:
			await interaction.followup.send(f"**آسف لا يمكنك إستخدام الزر فقط {self.view.author.mention}**", ephemeral=True)
			return
		
		data = db.duels.find_one({"_id": self.match_id})
		if not data:
			await interaction.followup.send("**بينات هذه المباراة لم تعد متاحة تم حذفها او تم تأكيد المباراة**", ephemeral=True)
			return
		player = await interaction.client.fetch_user(data["player"])
		opponent = await interaction.client.fetch_user(data["opponent"])
		channel = interaction.guild.get_channel(data["channel"])
		msg = await channel.fetch_message(data["msg"])
		
		if not self.author.id == player.id and not self.author.id == opponent.id and not helper.Helper.check_its_admin(self.author):
			await interaction.followup.send("**آسف فقط الآدمن او اصحاب المباراة يمكنهم حذفها شكرا**", ephemeral=True)
			return
		
		await interaction.followup.send(embed=embed(user=self.author, desc="هل انت متأكد من حذف هذه المباراة من قائدة البينات ؟", title="** • Duel system™ •**", icon_url=""), view=DuelDeleteConfirm(_id=self.match_id, author=self.author, player=player, opponent=opponent), ephemeral=True)


class DuelDeleteConfirm(View):
	def __init__(self, _id,author, player, opponent):
		super().__init__(timeout=120)
		self.author = author
		self.msg = None
		self.player = player
		self.opponent = opponent
		self.match_id = _id
	
	async def on_timeout(self):
		for b in self.children:
			b.disabled = True
		try:
			await self.msg.edit(view=self)
		except:
			pass
		
	@button(label="بكل تأكيد", style=ButtonStyle.green, emoji=emojis["yes"])
	async def accept(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user_inter = interaction.user
		
		data = db.duels.find_one({"_id":self.match_id})
		if not data:
			await interaction.followup.send("**بينات هذه المباراة لم تعد متاحة تم حذفها او تم تأكيد المباراة**", ephemeral=True)
			return
		channel = interaction.guild.get_channel(data["channel"])
		msg = await channel.fetch_message(data["msg"])
		
		if not user_inter.id == self.author.id:
			await  interaction.followup.send(embed=embed(user=user_inter, desc="اعتذر لا يمكنك إستخدام هذا الزر"), ephemeral=True)
			return 
		if not self.author.id == self.player.id and not self.author.id == self.opponent.id:
			alert = f"**- انتباه {self.player.mention} و {self.opponent.mention}\n- لقد خذف المباراة المسجلة بينكما بواسطة الإداري {self.author.mention}**"
		elif self.author.id == self.opponent.id:
			alert = f"**مرحبا {self.player.mention} يبدوا أن {self.opponent.mention} انشأتها ضده أرجو الا تكون هناك مشكلة**"
		else:
			alert = f"**- مرحبا {self.opponent.mention} يبدو ان {self.player.mention} قام بخذف هذه المباراة التي أنشاها ضدك  ارجو الا تكون هناك مشكلة**"
			
		db.duels.delete_one({"_id":self.match_id})
		self.on_timeout()
		await msg.reply(f">>> {alert}")
		await interaction.followup.send(embed=embed_done("تم حذف المباراة بنجاح لم تعد موجود في الملعب بعد الآن"), ephemeral=True)
		
	@button(label="لا الغاء", style=ButtonStyle.red, emoji=emojis["no"])
	async def cancel(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user_inter = interaction.user
		
		if not user_inter.id == self.author.id:
			await  interaction.followup.send(embed=embed(user=user_inter, desc="اعتذر لا يمكنك إستخدام هذا الزر"), ephemeral=True)
			return 
		
		await self.on_timeout()
		await interaction.followup.send(embed=embed_done("تم إلغاؤ العملية بنجاح"), ephemeral=True)
		

class DuelConfirm(View):
	def __init__(self, player, opponent, data):
		super().__init__(timeout=120)
		self.player = player
		self.opponent = opponent
		self.data = data
		self.msg = None
	
	async def Disabled(self):
		for b in self.children:
			b.disabled = True
	
	async def on_timeout(self):
		await self.Disabled()
		try:
			await self.msg.edit(view=self)
			await self.msg.reply(f"إنتهى الوقت تم  إلغاؤ الطلب تلقائيا بسبب عدم موافقة الاعب الثاني آسف {self.player.mention}")
		except:
			pass
		
	@button(label="نعم", style=ButtonStyle.green, emoji=emojis["yes"])
	async def confirm(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user_inter = interaction.user
		
		if user_inter.id == self.player.id:
			await interaction.followup.send(embed=embed(user=self.player, desc=f"تحلى بالصبر نحن ننتذر موافة {self.opponent.mention}"), ephemeral=True)
			return
		elif user_inter.id != self.opponent.id:
			await interaction.followup.send(embed=embed(user=user_inter, desc=f"اعتذر انت لست {self.opponent.mention}", title="**Duel system™**"), ephemeral=True)
			return
			
		em = embed(user=self.player, desc=f"تم تأكيد المباراة\n{self.player.mention} Vs {self.opponent.mention}\n نوع المباراة: {self.data['type']}\nالنقاط المتبادل: {emojis['points']} {self.data['points']}\n- تنبيه لا تحذفو هذه الرسالة 🚨", title="** • Duel system™ •**", icon_url="", image_url="https://cdn.discordapp.com/attachments/1249126837091696691/1303354912276742154/2b619e42172d1c0eab902cb7b20aa419b914830429f3dcb3dfb54a8a35b66e4e._SX1080_FMpng_.png")
		
		db.duels.insert_one(self.data)
		self.timeout = None
		await self.Disabled()
		await interaction.message.edit(f">>> **{self.player.mention} Vs {self.opponent.mention}**", embed=em, view=self)
		t = await interaction.message.reply("**يجب على الأدمن تأكيد المباراة بعد إنتهائها بالأمر التالي\n```/duels accept```**")
		await t.edit(content=t.content + "\n- @here")
	
	@button(label="لا", style=ButtonStyle.red, emoji=emojis["no"])
	async def cancel(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user_inter = interaction.user
		
		if user_inter.id == self.player.id:
			await interaction.followup.send(embed=embed(user=self.player, desc=f"تحلى بالصبر نحن ننتذر موافة {self.opponent.mention}"), ephemeral=True)
			return
		elif user_inter.id != self.opponent.id:
			await interaction.followup.send(embed=embed(user=user_inter, desc=f"اعتذر انت لست {self.opponent.mention}", title="**Duel system™**"), ephemeral=True)
			return
		
		self.timeout = None
		em = embed(user=self.player, desc=f"تم إلغاء طلب المباراة قام {self.opponent.mention} برفض الطلب\n- {self.player.mention} ربما عليك البحث عن لاعب والإتفاق معه قبل ذالك ", title="** • Duel system™ •**")
		await self.Disabled()
		await interaction.message.edit("تم رفض طلب المباراة (•_•)",embed=em, view=self)