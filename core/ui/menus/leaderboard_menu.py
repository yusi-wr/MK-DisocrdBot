from nextcord import ButtonStyle, Interaction, SelectOption
from nextcord.ui import View, Select, TextInput
from Config import emojis, images
from core import db, embeds


class SelectLeaderboard(Select):
	def __init__(self):
		super().__init__(placeholder="توب 10 متصدرين ؟", options=[
			SelectOption(label="نقاط المبارزة", emoji=emojis["points"], value="points"),
			SelectOption(label="نزلات/انتصارات", emoji=emojis["duel"], value="duels"),
			SelectOption(label="الفضة/ذهب", emoji=emojis["coins"], value="coins"),
			SelectOption(label="عودة للواجه", emoji=emojis["home"], value="home")
		])
		
	async def callback(self, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user_inter = interaction.user
		guild = interaction.guild
		
		if user_inter.id != self.view.author.id:
			await interaction.followup.send("**عذرا فقط {self.view.author.mention} يمكنه استخدام هذه\n\n- استخدم: #top**", ephemeral=True)
			return
		
		#frist_embed = interaction.message.embeds[0]
		data = {}
		fetchData = db.users.find({})
		
		if not fetchData:
			await interaction.followup.send("**لم يتم العثور على نتائج \nيبدو انه ليس لدينا اي لاعبين بعد ؟!**", ephemeral=True)
			return
		for user_data in fetchData:
			data[str(user_data["_id"])] = user_data
		
		match self.values[0]:
			case "points":
				sorted_data = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True)
				top_10 = sorted_data[:10]
				
				em = embeds.embed(user=guild.me, desc="هؤلاء هم المتصدرون من ناحية نقاط االمبارزة", title="**• توب عشر متصدرين نقاط المبارزة •**", icon_url="", image_url=images["bg"])
				
				for i, (user_id, user_data) in enumerate(top_10, start=1):
					user = guild.get_member(int(user_id))
					em.add_field(name=f"**المرتبة {i}**", value=f">>> **- الاعب: {user.mention if user is not None else'غيرموجود في الخادم'}\n- نقاط: {emojis['points']} {user_data['points']} نقطة**")
				author_id = str(user_inter.id)
				author_rank = next((i + 1 for i, (user_id, user_data) in enumerate(sorted_data) if user_id == author_id), None)
				
				text = f">>> **- مرتبتك: #{author_rank}\n- على: {len(sorted_data)}**"
				await interaction.message.edit(content=text,embed=em)
		
			case "duels":
				sorted_data = sorted(data.items(), key=lambda x: x[1]['duels']['count'], reverse=True)
				top_10 = sorted_data[:10]
				
				em = embeds.embed(user=guild.me, desc="هؤلاء هم المتصدرون من ناحية عدد المباريات", title="**• توب اعلى مباراة مسجلة •**", icon_url="", image_url=images["bg"])
				
				for i, (user_id, user_data) in enumerate(top_10, start=1):
					user = guild.get_member(int(user_id))
					em.add_field(name=f"**المرتبة {i}**", value=f">>> **- الاعب: {user.mention if user is not None else'غيرموجود في الخادم'}\n- المباريات: {user_data['duels']['count']}\n- انتصارات: {user_data['duels']['win']}\n- الخسارة: {user_data['duels']['lose']}**")
				author_id = str(user_inter.id)
				author_rank = next((i + 1 for i, (user_id, user_data) in enumerate(sorted_data) if user_id == author_id), None)
				
				text = f">>> **- مرتبتك: #{author_rank}\n- على: {len(sorted_data)}**"
				await interaction.message.edit(content=text,embed=em)
				
			case "coins":
				sorted_data = sorted(data.items(), key=lambda x: x[1]['coins'], reverse=True)
				top_10 = sorted_data[:10]
				
				em = embeds.embed(user=guild.me, desc="هؤلاء هم المتصدرون من ناحية عملة الفضية", title="**• توب عشر متصدرين فضة •**", icon_url="", image_url=images["bg"])
				
				for i, (user_id, user_data) in enumerate(top_10, start=1):
					user = guild.get_member(int(user_id))
					em.add_field(name=f"**المرتبة {i}**", value=f">>> **- الاعب: {user.mention if user is not None else'غيرموجود في الخادم'}\n- الفضة: {emojis['coins']} {user_data['coins']:,}$ فضة**")
				author_id = str(user_inter.id)
				author_rank = next((i + 1 for i, (user_id, user_data) in enumerate(sorted_data) if user_id == author_id), None)
				
				text = f">>> **- مرتبتك: #{author_rank}\n- على: {len(sorted_data)}**"
				await interaction.message.edit(content=text,embed=em)
			case "home":
				await interaction.message.edit(content="", embed=self.view.frist_embed)
			

class LeaderboardViewSelect(View):
	def __init__(self, author, frist_embed):
		super().__init__(timeout=None)
		self.author = author
		self.frist_embed = frist_embed
		self.add_item(SelectLeaderboard())
		