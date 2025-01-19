from nextcord import Interaction, ButtonStyle, Color, Embed
from nextcord.ui import Button, button, View
from Config import emojis
from core.embeds import embed
from core.database import db


class ButtonSuggestion(View):
	def __init__(self):
		super().__init__(timeout=None)
		
	@button(label="0", style=ButtonStyle.green, emoji=emojis["yes"], custom_id="suggestion-up")
	async def Up(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		_id = interaction.message.id
		data = db.suggetions.find_one({"_id": _id})
		if user.mention in data["dwon"]:
			await interaction.followup.send(content="**-  إضغط الزر الآخر لإلغاء التصويت اولا 🙂**", ephemeral=True)
			return
		
		if user.mention in data["up"]:
			data["up"].remove(user.mention)
			await interaction.followup.send(content="**تم الغاؤ التصويت بنجاح 😁**", ephemeral=True)
		else:
			data["up"].append(user.mention)
			await interaction.followup.send(content="**- تم التصويت بنجاح 😁**", ephemeral=True)
		
		button.label = str(len(data["up"]))
		await interaction.message.edit(view=self)
		db.suggetions.update_one({"_id":_id}, {"$set": data})
		
	@button(label="0", style=ButtonStyle.red, emoji=emojis["no"], custom_id="suggestion-dwon")
	async def Dwon(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		_id = interaction.message.id
		data = db.suggetions.find_one({"_id": _id})
		if user.mention in data["up"]:
			await interaction.followup.send(content="**-  إضغط الزر الآخر لإلغاء التصويت اولا 🙂**", ephemeral=True)
			return
		if user.mention in data["dwon"]:
			data["dwon"].remove(user.mention)
			await interaction.followup.send(content="**تم الغاؤ التصويت بنجاح 😁**", ephemeral=True)
		else:
			data["dwon"].append(user.mention)
			await interaction.followup.send(content="**- تم التصويت بنجاح 😁**", ephemeral=True)
			
		button.label = str(len(data["dwon"]))
		await interaction.message.edit(view=self)
		db.suggetions.update_one({"_id":_id}, {"$set": data})
		
	@button(label="الإحصائية", style=ButtonStyle.gray, emoji=emojis["stats"], custom_id="suggestion-stats")
	async def Stats(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		_id = interaction.message.id
		data = db.suggetions.find_one({"_id": _id})
		text_up = "- " + "\n- ".join(x for x in data["up"])
		text_dwon = "- " + "\n- ".join(x for x in data["dwon"])
		
		if text_dwon == "- ":
			text_dwon = "- 0"
		if text_up == "- ":
			text_up = "- 0"
			
		em = Embed(color=Color.random())
		em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1300922260412043336.png")
		em.add_field(name=f"**مقبول: 👍 {len(data['up'])}**", value=f"**{text_up}**")
		em.add_field(name=f"**مرفوض: 👎  {len(data['dwon'])}**", value=f"**{text_dwon}**")
		em.set_footer(text=f"تم انشاؤه في: {data['date'].split('.')[0]}")
		await interaction.followup.send(embed=em, ephemeral=True)
		
	@button(label="حذف", style=ButtonStyle.gray, emoji=emojis["delete"], custom_id="delete-suggestion")
	async def Delete(self, button: Button, interaction: Interaction):
		from core.helper import Helper
		await interaction.response.defer(ephemeral=True)
		_id = interaction.message.id
		if Helper.check_its_admin(interaction.user):
			db.suggetions.delete_one({"_id":interaction.message.id})
			await interaction.message.delete()
		else:
			await interaction.followup.send("**عذرا لا تمللك صلاحيات لفعل هذا**", ephemeral=True)