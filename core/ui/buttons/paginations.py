from nextcord.ui import Button, View, button
from nextcord import Interaction, ButtonStyle, Embed
from Config import emojis, config
from random import choice

class PaginatorEmbeds(View):
	def __init__(self, embeds, author, names=None):
		super().__init__(timeout=120)
		
		self.page = 1
		self.embeds = embeds
		self.author = author
		self.names = names
		
	async def on_timeout(self):
		for btn in self.children:
			btn.disabled = True
		try:
			await self.msg.edit(view=self)
		except:
			pass
		
	@button(style=ButtonStyle.gray,emoji=emojis["backward"])
	async def BackWard(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(f"آسف فقط {self.author.mention} يمكنه إستخدام الزر")
			return
		self.page -= 1
		if self.page < 1:
			self.page = len(self.embeds)
		
		embed: Embed = self.embeds[self.page - 1]
		self.PageHand.label = f"{len(self.embeds)}/{self.page}"
		await interaction.message.edit(embed=embed, view=self)
	
	#button for back to home or page 1
	@button(style=ButtonStyle.red, emoji=emojis["home"])
	async def Home(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(f"آسف فقط {self.author.mention} يمكنه إستخدام الزر")
			return
			
		self.page = 1
		embed: Embed = self.embeds[self.page - 1]
		self.PageHand.label = f"{len(self.embeds)}/{self.page}"
		await interaction.message.edit(embed=embed, view=self)
	
	#button hand page
	@button(label="?/1", style=ButtonStyle.grey, disabled = True)
	async def PageHand(self, button: Button, interaction: Interaction):
		pass
	
	#Forward button
	@button(style=ButtonStyle.grey, emoji=emojis["forward"])
	async def Ward(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(f"آسف فقط {self.author.mention} يمكنه إستخدام الزر")
			return
			
		self.page += 1
		if self.page > len(self.embeds):
			self.page = 1
			
		embed: Embed = self.embeds[self.page - 1]
		self.PageHand.label = f"{len(self.embeds)}/{self.page}"
		await interaction.message.edit(embed=embed, view=self)
		
	@button(style=ButtonStyle.red, emoji=emojis["cancel"])
	async def Cancel(self, button: Button, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		
		if user.id != self.author.id:
			await interaction.followup.send(f"آسف فقط {self.author.mention} يمكنه إستخدام الزر")
			return
			
		await self.on_timeout()
		await interaction.message.edit(view=None)
		
	
	
		