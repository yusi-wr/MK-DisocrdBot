from nextcord import ButtonStyle, Interaction,  Embed, SelectOption
from nextcord.ui import Button, button, Modal, View, Select, TextInput
from core.ui import buttons

#class Modal for choice pages
class ModalPage(Modal):
	def __init__(self,  embeds: list, name_lists: list, origin_inte: Interaction, author):
		super().__init__(title="الإنتقال الى الصفحة؟")
		
		self.embeds = embeds
		self.author = author
		self.names = name_lists
		self.origin_inte = origin_inte
		
		self.page = TextInput(
		     label="اكتب رقم الصفحة",
		     min_length=1,
		     max_length=2,
		     required=True,
		     placeholder="1 او 3 او 4"
		)
		self.add_item(self.page)
		
	async def callback(self, interaction: Interaction):
		
		if int(self.page.value) > len(self.embeds):
			await interaction.response.send_message(content=f"**اعتذر يجب ادخال رقم ليس اعلى من عدد الصفحات: {len(self.embeds)}**", ephemeral=True)
			return
			
		user = interaction.user
		page = int(self.page.value)
		embed: Embed = self.embeds[page - 1]
		pages = Embed(title="**📑 الصفحة: {page}/{embeds}**".format(page=page, embeds=len(self.embeds)))
		
		await interaction.message.edit(embeds=[embed, pages], view=buttons.CardsPage(embeds=self.embeds, name_lists=self.names, author=self.author, origin_inte=self.origin_inte,page=page))