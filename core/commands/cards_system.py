from nextcord.ext import commands
from nextcord import Interaction
from core.cards.collections import *
from core.cards import Card
from random import choice
from core.ui import buttons
from core.cards import CardsGame
from core.helper import Helper

#class commands functions
class CommandCardsSystem():
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#function
	async def GameCard(self, interaction: Interaction, archetype: str = None):
		"""Simple game card function command"""
		await interaction.response.defer() 
		archetype_list_name =  archetypes[archetype] if archetype else None
		await CardsGame(interaction=interaction, archetype=archetype_list_name)
	
	#command function	
	async def NormalSearch(self, interaction: Interaction, name=None, card_id=None):
		"""Function command searching one card"""
		await interaction.response.defer()
		try:
			if name:
				card = cards_data[name]
			else:
				card = cards_data[cards_id[str(card_id)]] if str(card_id) in cards_id else cards_data[cards_id[str(Helper.fuzzy(card_id, [ids for ids in cards_id], results=1)[0])]]
			
			result_data = Card(card=card, guild=interaction.guild)
			await interaction.followup.send(embed=await result_data.embed_cards(), view=buttons.ButtonCards(embeds_sets=await result_data.embeds_cards_sets(), name=name, author=interaction.user, origin_inte=interaction))
		except Exception as Errer:
			await Helper.CardsNoResult(interaction)
	
	#function
	async def RandomCard(self, interaction: Interaction):
		"""Function command get a random card"""
		await interaction.response.defer()
		try:
			name = choice(cards_name)
			card = Card(card=cards_data[name], guild=interaction.guild)
			await interaction.followup.send(embed=await card.embed_cards(), view=buttons.ButtonCards(embeds_sets=await card.embeds_cards_sets(), author=interaction.user, origin_inte=interaction, name=name))
		except Exception as Error:
			await Helper.CardsNoResult(interaction)
			
	#function
	async def ArtSearch(self, interaction: Interaction, name):
		"""Functions get cards art`s by name"""
		await interaction.response.defer()
		try:
			card = Card(card=cards_data[name], guild=interaction.guild)
			
			Images = [cards_art[i]["url"] for i in cards_art if cards_art[i]["name"] == name]
			embed_card = await card.embed_arts()
			if len(Images) > 1:
				await interaction.followup.send(embed=embed_card, view=buttons.CardsImagePage(embed=embed_card, author=interaction.user, images=Images, origin_inte=interaction))
			else:
				await interaction.followup.send(embed=embed_card)
		except Exception as Error:
			await Helper.CardsNoResult(interaction=interaction, error=Error)
			
	#function
	async def ArtRandom(self, interaction: Interaction):
		"""Functions get cards art`s by random"""
		await interaction.response.defer() 
		try:
			name = choice(cards_name)
			card = Card(card=cards_data[name], guild=interaction.guild)
			
			Images = [cards_art[i]["url"] for i in cards_art if cards_art[i]["name"] == name]
			embed_card = await card.embed_arts()
			if len(Images) > 1:
				await interaction.followup.send(embed=embed_card, view=buttons.CardsImagePage(embed=embed_card, author=interaction.user, images=Images, origin_inte=interaction))
			else:
				await interaction.followup.send(embed=embed_card)
		except Exception as Error:
			await Helper.CardsNoResult(interaction=interaction, error=Error)
			
	#function
	async def ImageSearch(self, interaction: Interaction, name):
		"""Functions get cards art`s by name"""
		await interaction.response.defer() 
		try:
			card = Card(card=cards_data[name], guild=interaction.guild)
			
			Images = [cards_images[i]["url"] for i in cards_images if cards_images[i]["name"] == name]
			embed_card = await card.embed_normal_images()
			if len(Images) > 1:
				await interaction.followup.send(embed=embed_card, view=buttons.CardsImagePage(embed=embed_card, author=interaction.user, images=Images, origin_inte=interaction))
			else:
				await interaction.followup.send(embed=embed_card)
		except Exception as Error:
			await Helper.CardsNoResult(interaction=interaction, error=Error)
	
	#function
	async def ArchetypeSearch(self, interaction: Interaction,  archetype: str):
		"""Function command for get all cards in the archetype"""
		await interaction.response.defer() 
		try:
			guild = interaction.guild
			user = interaction.user
			if archetype not in archetypes:
				await Helper.CardsNoResult(interaction)
				return
				
			cards_list = sorted(archetypes[archetype])
			
			card = Card(card=cards_data[cards_list[0]], guild=guild)
			embeds = [await Card(cards_data[c], guild).embed_cards() for c in cards_list]
			
			msg  = await interaction.followup.send(embed=await card.embed_cards(), view=buttons.CardsPage(embeds=embeds, name_lists=cards_list, origin_inte=interaction, author=user))
		except Exception as Error:
			await Helper.CardsNoResult(interaction=interaction, error=Error)
		
		