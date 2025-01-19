from core import stores, helper
import core
from core.database import db
from core.embeds import embed, embed_done
from Config import emojis, config
from nextcord import Interaction, ButtonStyle, Member
from nextcord.ui import Button, button, View
from random import randint


class ButtonPoints(Button):
	def __init__(self, points, price, author):
		super().__init__(label=f"{points}", style=ButtonStyle.gray, emoji=emojis["points"])
		self.price = price
		self.author = author
		
	async def callback(self, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		userData = helper.Helper.get_user_data(user)
		
		points = int(self.label) + randint(2, 7)
		
		if user.id != self.author.id:
			await interaction.followup.send(f"آسف فقط {self.view.author.mention} يمكنه إستخدام الزر", ephemeral=True)
			return
		if userData["coins"] < self.price:
			await interaction.followup.send(embed=embed(user=user, desc=f"لا تملك ما يكفي من الفضة لشراء {points} نقطة"), ephemeral=True)
			return
		
		userData["points"] += points
		userData["coins"] -= self.price
		update = {
			"$set": {
				"coins": userData["coins"],
				"points": userData["points"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await interaction.followup.send(embed=embed_done(desc=f"لقد إشتريت {emojis['points']} {points} نقطة\n- نقاطك حاليا {emojis['points']} {userData['points']}"), ephemeral=True)
		

class ViewPoints(View):
	def __init__(self, store: dict, author):
		super().__init__(timeout=120)
		self.author = author
		
		for key, val in store.items():
			self.add_item(ButtonPoints(points=key, price=val, author=author))
		
	async def on_timeout(self):
		for btn in self.children:
			btn.disabled = True
		try:
			await self.msg.edit(view=self)
		except:
			pass


class BuyItems(Button):
	def __init__(self, items_id = None):
		super().__init__(label="شراء", style=ButtonStyle.green, emoji=emojis["buy"])
		
		self.item_id = items_id
		
	async def callback(self, interaction: Interaction):
		await interaction.response.defer(ephemeral=True)
		user = interaction.user
		userData = helper.Helper.get_user_data(user)
		
		if user.id != self.view.author.id:
			await interaction.followup.send(f"آسف فقط {self.view.author.mention} يمكنه إستخدام الزر", ephemeral=True)
			return
		
		if self.item_id:
			item_id = self.item_id
		else:
			item_id = self.view.names[self.view.page - 1]
			
		itemdata = stores.items[item_id]
		if len(userData["items"]) == userData["bagmax"] and item_id not in userData["items"]:
			await interaction.followup.send(embed=embed(user=user, desc="أعتذر حقيبة الآيتمس ممتلعة يجب عليك إستخدام بعضها او إشراء `رفع المستوى` من المتجر"), ephemeral=True)
			return
		if userData["coins"] < itemdata["price"]:
			await interaction.followup.send(embed=embed(user=user, desc="لا تملك ما يكفي من الفضة لشراء هذا الغرض", title="**فشل عملية الشراء*"), ephemeral=True)
			return
		
		amount = itemdata["amount"]
		check = core.items.Check(user, "207")
		if check:
			befor = amount
			amount = amount * 2
			textEffect = f"تفعيل التأثير\n- تم مضاعفة الكمية من {befor} الى {amount} بسبب تأثير `{check['name']}`"
		else:
			textEffect = None
		if item_id  in userData["items"]:
			userData["items"][item_id]["amount"] += amount
		else:
			userData["items"][item_id] = {}
			userData["items"][item_id]["amount"] = amount
			
		userData["coins"] -= itemdata["price"]
		update = {
			"$set": {
				"coins": userData["coins"],
				"items": userData["items"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await interaction.followup.send(embed=embed_done(desc=f"تم الشراء بنجاح لقد إشتريت `{itemdata['name']}`"), ephemeral=True)
		if check:
			await interaction.followup.send(embed=embed(user=user,desc=textEffect, title=f"** • {check['name']} • **", icon_url=check["icon"]), ephemeral=True)