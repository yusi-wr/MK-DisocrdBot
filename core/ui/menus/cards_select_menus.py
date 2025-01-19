from nextcord.ext.commands import Bot
from nextcord import ButtonStyle, Interaction,  Embed, SelectOption
from nextcord.ui import Button, button, Modal, View, Select, TextInput
from random import choice
from Config import config, emojis
from core.ui import buttons
from core.cards import Card
from core.cards.collections import cards_data

#----------------(SelectMenu class`s)
class CardsSelectMenu(Select):
	"""Select menu for search cards by name"""
	def __init__(self, names, author, origin_inte):
		super().__init__(
		placeholder="Select card", 
		options=[SelectOption(label=name, emoji=emojis["card"]) for name in names]
		)
		self.author = author
		self.names = names
		self.origin_inte = origin_inte
	async def callback(self, interaction:  Interaction):
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.response.send_message(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
		
		if self.values:
			card = Card(cards_data[self.values[0]], interaction.guild)
			view = buttons.ButtonCards(embeds_sets=await card.embeds_cards_sets(), name=self.values[0], author=self.author, origin_inte=self.origin_inte)
			view.add_item(self)
			await interaction.message.edit(embed=await card.embed_cards(), view=view)