from nextcord.ext.commands import Bot
from nextcord import ButtonStyle, Interaction,  Embed, SelectOption
from nextcord.ui import Button, button, Modal, View, Select, TextInput
from .paginations import PaginatorEmbeds
from random import choice
from Config import config, emojis
from core.ui import modals
from core.ui import menus
from core.embeds import embed
from core.cards.collections import cards_data, cards_name
from core.cards import Card


#---------------(View class`s)----------------
#calss button cards
class ButtonCards(View):
	def __init__(self, origin_inte: Interaction, embeds_sets, name, author):
		super().__init__(timeout=60 * 10)
		
		self.author = author
		self.origin_inte = origin_inte
		self.name = name
		self.embeds_sets = embeds_sets
		self.translate = "ar"
		
	async def on_timeout(self):
		for btn in self.children:
			btn.disabled = True
		try:
			await self.origin_inte.edit_original_message(view=self)
		except:
			pass
	
	#search cards list
	@button(label="بحث", style=ButtonStyle.gray, emoji=emojis["search"])
	async def SearchingList(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
		
		from core.helper import Helper
		names = await Helper.fuzzy(comparate=self.name, comparables=cards_name, results=25)
		
		card = Card(cards_data[names[1]], interaction.guild)
		view = ButtonCards(embeds_sets=await card.embeds_cards_sets(), name=names[1], author=user, origin_inte=self.origin_inte)
		view.add_item(menus.CardsSelectMenu(names=names, author=self.author, origin_inte=self.origin_inte))
		await interaction.message.edit(embed=await card.embed_cards(), view=view)
		
	#@button(label="ترجمة",style=ButtonStyle.gray, emoji=emojis["translate"])
#	async def Translate(self, button: Button, interaction: Interaction):
#		await interaction.response.defer(ephemeral=True)
#		user = interaction.user
#		
#		if user.id != self.author.id:
#			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
#			return
#		
#		card = Card(card=cards_data[self.name], guild=interaction.guild)
#		if self.translate == "ar":
#			embed = await card.embed_cards_ar()
#			self.translate = "en"
#		else:
#			embed = await card.embed_cards()
#			self.translate = "ar"
#		await interaction.message.edit(embed=embed)
		
	#button get cards sets
	@button(label="السيت", style=ButtonStyle.gray, emoji=emojis["list"])
	async def GetRare(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
		
		if self.embeds_sets is not None:
			if len(self.embeds_sets) > 1:
				view = PaginatorEmbeds(embeds=self.embeds_sets, author=user)
				view.add_item(ButtonDelete(user))
				await interaction.followup.send(embed=self.embeds_sets[0], view=view)
			else:
				view=View()
				view.add_item(ButtonDelete(author=self.author))
				await interaction.followup.send(embed=self.embeds_sets[0], view=view)
		else:
			await interaction.followup.send(embed=embed(user=user,desc="لم يتم الأثور على أي نتائج يرجى المحاولة من جديد"), ephemeral=True)
	

#class button pages for search by  archetype
class CardsPage(View):
	def __init__(self, embeds: list, name_lists: list, origin_inte: Interaction, author, page=None):
		super().__init__(timeout=60 * 10)
		
		self.names = name_lists
		self.embeds = embeds
		self.page = page if page else 1
		self.origin_inte = origin_inte
		self.author = author
		self.translate = "ar"
		
	async def on_timeout(self):
		for btn in self.children:
			btn.disabled = True
		await self.origin_inte.edit_original_message(view=self)	
	
	#backward button
	@button(style=ButtonStyle.grey, emoji=emojis["backward"])
	async def Back(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		self.page -= 1
		if self.page < 1:
			self.page = len(self.embeds)
			
		em: Embed = self.embeds[self.page - 1]
		page = Embed(title="**الصفحة: {page}/{embeds}**".format(page=self.page, embeds=len(self.embeds)))
		self.translate = "ar"
		await interaction.message.edit(embeds=[em, page], view=self)
	
	#button for back to home or page 1
	@button(style=ButtonStyle.red, emoji=emojis["home"])
	async def Home(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		self.page = 1
		em: Embed = self.embeds[self.page - 1]
		page = Embed(title="**الصفحة: {page}/{embeds}**".format(page=self.page, embeds=len(self.embeds)))
		self.translate = "ar"
		await interaction.message.edit(embeds=[em, page], view=self)
		
	#button  for go to page by modal
	@button(style=ButtonStyle.red, emoji=emojis["list"])
	async def GoToPage(self, button: Button, interaction: Interaction):
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.response.send_message(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		await interaction.response.send_modal(modals.ModalPage(embeds=self.embeds, name_lists=self.names, origin_inte=self.origin_inte, author=self.author))
			
	#Forward button
	@button(style=ButtonStyle.grey, emoji=emojis["forward"])
	async def Ward(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		self.page += 1
		if self.page > len(self.embeds):
			self.page = 1
			
		em: Embed = self.embeds[self.page - 1]
		page = Embed(title="**الصفحة: {page}/{embeds}**".format(page=self.page, embeds=len(self.embeds)))
		self.translate = "ar"
		await interaction.message.edit(embeds=[em, page], view=self)
		
	#@button(label="ترجمة",style=ButtonStyle.gray, emoji=emojis["translate"])
#	async def Translate(self, button: Button, interaction: Interaction):
#		await interaction.response.defer(ephemeral=True)
#		user = interaction.user
#		
#		if user.id != self.author.id:
#			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
#			return
#		
#		card = Card(card=cards_data[self.names[self.page - 1]], guild=interaction.guild)
#		if self.translate == "ar":
#			embed = await card.embed_cards_ar()
#			self.translate = "en"
#		else:
#			embed = await card.embed_cards()
#			self.translate = "ar"
#		await interaction.message.edit(embed=embed)
	
	#button get cards sets
	@button(label="السيت", style=ButtonStyle.gray, emoji=emojis["list"])
	async def GetRare(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
		
		card = Card(cards_data[self.names[self.page - 1]], interaction.guild)
		embeds = await card.embeds_cards_sets()
		if embeds is not None:
			if len(embeds) > 1:
				view = PaginatorEmbeds(embeds=embeds, author=user)
				view.add_item(ButtonDelete(user))
				await interaction.followup.send(embed=embeds[0], view=view, ephemeral=True)
			else:
				view=View()
				view.add_item(ButtonDelete(author=self.author))
				await interaction.followup.send(embed=embeds[0], view=view, ephemeral=True)
		else:
			await interaction.followup.send(embed=embed(user=user,desc="لم يتم الأثور على أي نتائج يرجى المحاولة من جديد"), ephemeral=True)

#class button pages image list
class CardsImagePage(View):
	def __init__(self, images: list, embed, origin_inte: Interaction, author, page=None):
		super().__init__(timeout=180)
		
		self.images = images
		self.page = page if page else 1
		self.origin_inte=origin_inte
		self.author = author
		self.embed = embed
		
	async def on_timeout(self):
		for btn in self.children:
			btn.disabled = True
		await self.origin_inte.edit_original_message(view=self)	
	
	#backward button
	@button(style=ButtonStyle.grey, emoji=emojis["backward"])
	async def Back(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			
		self.page -= 1
		if self.page < 1:
			self.page = len(self.images)
			
		self.embed.set_image(url=self.images[self.page - 1])
		
		await interaction.message.edit(embed=self.embed)
	
	#button for back to home or page 1
	@button(style=ButtonStyle.red, emoji=emojis["home"])
	async def Home(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		self.page = 1
		self.embed.set_image(url=self.images[self.page - 1])
		
		await interaction.message.edit(embed=self.embed)
			
	#Forward button
	@button(style=ButtonStyle.grey, emoji=emojis["forward"])
	async def Ward(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		self.page += 1
		if self.page > len(self.images):
			self.page = 1
		self.embed.set_image(url=self.images[self.page - 1])
		
		await interaction.message.edit(embed=self.embed)

#---------------(Simple buttons)
class ButtonDelete(Button):
	"""This button for get sets code for any cards"""
	def __init__(self, author):
		super().__init__(style=ButtonStyle.red,emoji=emojis["delete"])
		self.author = author
	
	async def callback(self, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(content="اعتذر فقط {user} من يمكنه اتستخدام الزر".format(user=user.mention), ephemeral=True)
			return
			
		await interaction.message.delete()

