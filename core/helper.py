from nextcord.ext import commands
from nextcord import Guild, Member, Interaction, File, Message
import requests
from difflib import get_close_matches
from colorama import Fore, Style
from string import punctuation
import os

from Config import config, emojis
from datetime import datetime, timedelta
import humanfriendly
from core import db
from core.stores import items
from core.embeds import embed
#from core.ui import buttons
from core.cards.collections import cards_data, cards_id, cards_art, cards_images, cards_name, archetypes
from core.cards  import Card

class Helper:
	#-----------(Normal Functions)
	
	#function 
	@classmethod
	def ItemsList(self):
		d =  {}
		for key, vals in items.items():
			d[vals["name"]] = key
		return d
	
	#function
	@classmethod
	def check_its_admin(self, user: Member, owner_only=False):
		"""فحص اليوسر نشوف إذا هو ادمن او أونير"""
		from bot import bot
		guild = user.guild
		settings = self.guild_settings(guild)
		admin_roles = [guild.get_role(r) for r in settings["admin_roles"]]
		if owner_only:
			return user.id in bot.owner_ids or user.id == guild.owner.id
		else:
			return any(role in user.roles for role in admin_roles) or user.id in bot.owner_ids or user.id == guild.owner.id
	
	#function
	@classmethod
	def guild_settings(self, guild: Guild):
			"""جلب اعدادات الخادم في  اي وقت"""
			defualt = {
			"_id": guild.id,
			"admin_roles": [],
			"boost_channel": None,
			"boost_msg": None,
			"channel_news": None,
			"auto_line_channels": [],
			"suggestion_channel": None,
			"channel_news": None,
			"youtube": {
				"channel": None,
				"data": {}
				}
			}
			
			key = {"_id":guild.id}
			if not db.settings.find_one(key):
				db.settings.insert_one(defualt)
			
			return db.settings.find_one(key)
	
	#function
	@classmethod
	def get_user_data(self, user):
		"""جلب او انشاء معلومات اليوسر في اي وقت"""
		defualt = {
			"_id": user.id,
			"name": None,
			"coins": 5000,
			"points": 50,
			"lp": 100,
			"cup": 0,
			"bg": None,
			"icon": None,
			"rep": 0,
			"bagmax": 3,
			"warns": 0,
			"duels": {
				"count": 0,
				"win": 0,
				"lose": 0
				},
			"items": {},
			"activite": {}
			}
		
		if not db.users.find_one({"_id":user.id}):
			db.users.insert_one(defualt)
		return db.users.find_one({"_id":user.id})
	
	#function
	@classmethod
	def get_cooldwon_time(self, user, cmd, items=False):
		"""Simple function for get user cooldwon time/hour"""
		if items == True:
			row = "items"
		else:
			row = "cmds"
			
		find_key = {"_id":user.id}
		data = db.cooldwons.find_one(find_key)[row]
		type_ms = humanfriendly.parse_timespan(f"{str(data[cmd]['type'])}h")
		
		getdate = datetime.strptime(str(data[cmd]["date"]), "%Y-%m-%d %H:%M:%S.%f")
		diff = datetime.utcnow() - getdate
		date = str(timedelta(seconds=type_ms - diff.total_seconds())).split(".")[0]
		return date
	
	#function
	@classmethod
	def formter_other_time(self, oldDate, time_type: str):
		type_ms = humanfriendly.parse_timespan(time_type)
		
		getdate = datetime.strptime(oldDate, "%Y-%m-%d %H:%M:%S.%f")
		diff = datetime.utcnow() - getdate
		date = str(timedelta(seconds=type_ms - diff.total_seconds())).split(".")[0]
		return date
	
	#function
	@classmethod
	def format_rank(self, points):
		if points >= 30 and points < 240:
			return emojis["ranks"]["bronze"]
		elif points >= 240 and points < 460:
			return emojis["ranks"]["silver"]
		elif points >= 460 and points < 610:
			return emojis["ranks"]["gold"]
		elif points >= 610 and points < 810:
			return emojis["ranks"]["platinum"]
		elif points >= 810 and points < 1100:
			return emojis["ranks"]["daimond"]
		elif points >= 1100 and points < 2100:
			return emojis["ranks"]["master"]
		elif points >= 2100:
			return emojis["ranks"]["legend"]
		else:
			return emojis["ranks"]["noob"]
		
	#function
	@classmethod
	def foramt_health(self, health):
		if health <= 10 and health < 20 and health > 0:
			return emojis["health"]["1"] + f" {str(health)}%"
		elif health >= 20 and health < 30:
			return emojis["health"]["2"] + f" {str(health)}%"
		elif health >= 30 and health < 40:
			return emojis["health"]["3"] + f" {str(health)}%"
		elif health >= 40 and health < 50:
			return emojis["health"]["4"] + f" {str(health)}%"
		elif health >= 50 and health < 60:
			return emojis["health"]["5"] + f" {str(health)}%"
		elif health >= 60 and health < 70:
			return emojis["health"]["6"] + f" {str(health)}%"
		elif health >=70 and health < 80:
			return emojis["health"]["7"] + f" {str(health)}%"
		elif health >= 80 and health < 90:
			return emojis["health"]["8"] + f" {str(health)}%"
		elif health >= 90 and health < 100:
			return emojis["health"]["9"] + f" {str(health)}%"
		elif health >= 100 and health < 120:
			return emojis["health"]["10"] + f" {str(health)}%"
		elif health > 120:
			return emojis["health"]["double"] + f" {str(health)}%"
		else:
			return emojis["health"]["0"] + f" {str(health)}%"
	
	#function
	@classmethod
	def check_cooldwon(self, user, cmd: str, type: int, items=False):
		"""For check user cooldwon and """
		if items == True:
			row = "items"
		else:
			row = "cmds"
		defualt = {
		  "_id": user.id,
		  "cmds": {},
		  "items": {}
		}
		find_key = {"_id":user.id}
		if not db.cooldwons.find_one(find_key):
			db.cooldwons.insert_one(defualt)
		data = db.cooldwons.find_one(find_key)[row]
		
		if not cmd in data:
			data[cmd] = {}
			data[cmd]["date"] = str(datetime.utcnow())
			data[cmd]["type"] = type
			db.cooldwons.update_one({"_id":user.id}, {"$set":{row:data}})
			return True
		else:
			oldDate = data[cmd]["date"]
			type = data[cmd]["type"]
			date = datetime.strptime(oldDate, "%Y-%m-%d %H:%M:%S.%f")
			diff = datetime.utcnow() - date
			
			if (diff.total_seconds() / 3600) >= type:
				data[cmd]["date"] = str(datetime.utcnow())
				db.cooldwons.update_one({"_id":user.id}, {"$set":{row:data}})
				return True
			else:
				return False
	
	#function
	@classmethod
	def CheckItemsTime(self, oldDate: str, hour_type: int):
		"""For check items tems and """
		date = datetime.strptime(oldDate, "%Y-%m-%d %H:%M:%S.%f")
		diff = datetime.utcnow() - date
		
		if (diff.total_seconds() / 3600) >= hour_type:
			return True
		else:
			return False
			
	#function
	@classmethod
	def get_user_profile(self, user: Member):
		userData = self.get_user_data(user)
		
		health = self.foramt_health(userData["lp"])
		rank = self.format_rank(userData["points"])
		points = userData["points"]
		coins = userData["coins"]
		name = userData["name"]
		cups = userData["cup"]
		maxbag = userData["bagmax"]
		countItems = len(userData["items"])
		rep = userData["rep"]
		warns = userData["warns"]
		bg = userData["bg"]
		icon = userData["icon"]
		duelsCount = userData["duels"]["count"]
		duelsWin = userData["duels"]["win"]
		duelsLose = userData["duels"]["lose"]
		if bg is None:
			bg = config["images"]["bg"]
		if icon is None:
			icon = user.avatar.url
		if not name:
			name = user.display_name
		else:
			name = f"**• {emojis['stareffct']} {name} {emojis['stareffct']} •**"
		
		em = embed(user=user,
			desc=f"- الفضة: {emojis['coins']} {coins:,}$\n- نقاط المبارزة: {emojis['points']} {points:,}\n- عدد الكؤوس: {emojis['cup']} {cups}\n- الرنك: {rank}\nنقاط الصحة: {health}\n- نقاط السمعة: {emojis['rep']} {rep}\n- الحقيبة: {emojis['bag']} {maxbag}/{countItems}\n- الإنظاراة: {emojis['warns']} {warns}",
			title=name, 
			icon_url=icon,
			image_url=bg
		)
		em.add_field(name=f"** • {emojis['duel']} النزالات {duelsCount} •**",  value=f">>> **- الإنتصارات: {duelsWin:,}\n- الخسارة: {duelsLose:,}**")
		return em
	
	#---------------(Async functions)
	
	@classmethod
	async def CardsNoResult(self, interaction: Interaction, error=None):
		  """Return for message any time if the not found the cards"""
		  user = interaction.user
		  em=embed(user=user,desc="لم يتم الأثور على أي نتائج يرجى المحاولة من جديد" + f"\n**اخطاء اخرى**\n```{error if error else 'لا شيء'}```")
		  
		  try:
		  	await interaction.message.edit(embed=em)
		  except:
		  	await interaction.followup.send(embed=em)
	
	@classmethod
	async def clean(self, text):
   	 '''Remove punctuation and unicode from the text, convert it to lowercase and return it'''
   	 return (
      	  ' '.join(text.translate(str.maketrans({mark : ' ' for mark in punctuation})).split())
           .encode('ascii', 'ignore')
           .decode()
           .lower()
           )
	
	@classmethod
	async def fuzzy(self, comparate, comparables, results=25):
	    '''Compare the comparate with the comparables and return results''' 
	    return get_close_matches(comparate, comparables, cutoff=0.1, n=results)
	
	@classmethod
	async def update_cards(self, bot: commands.Bot):
		"""function update cards data 24/7"""
		ygopro_deck = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
		data = requests.get(url=ygopro_deck, params={"misc":"yes"}).json()["data"]
		
		if data:
			cards_data.clear()
			cards_art.clear()
			cards_id.clear()
			cards_images.clear()
			cards_name.clear()
			
			for card in data:
				name = await self.clean(card["name"])
				ID = card["id"]
				cards_data[name] = card
				cards_name.append(name)
				
				if "archetype" in card:
					Archetype = await self.clean(card["archetype"])
					if Archetype in archetypes:
						archetypes[Archetype].append(name)
					else:
						archetypes[Archetype] = []
						archetypes[Archetype].append(name)
				
				for images in card["card_images"]:
					image_id =  str(images["id"])
					cards_images[image_id] = {}
					cards_images[image_id]["name"] = name
					cards_images[image_id]["url"] = images["image_url"]
					cards_art[image_id] = {}
					cards_art[image_id]["name"] = name
					cards_art[image_id]["url"] = images["image_url_cropped"]
					cards_id[image_id] = name
					
			count_cards = len(cards_name)
			print(f"{Fore.LIGHTMAGENTA_EX} • Done Update:" + f"{Fore.LIGHTGREEN_EX} {count_cards:,}" + f"{Fore.LIGHTMAGENTA_EX} Cards successfuly ✓")
	
	
	#function
	@classmethod
	async def send_image_lines(self, channel, image, add_here_mention=True):
		send = await channel.send(file=File(f"./assets/{image}"))
		if add_here_mention:
			await send.edit("@here")
	
	#function
	@classmethod
	async def not_has_permisions(self, ctx: commands.Context=None, inter: Interaction = None, for_owner=False):
		"""فونكشن للرد على المستخدم إذا لم يكن مشرف او owner"""
		if for_owner:
			msg = "- {0} اعتذر لكن هذا االأمر مخصص للأونرس فقط سوري ".format(emojis["no"])
		else:
			msg = "- {0} اعتذر لكن هذا االأمر مخصص فقط للأدمنس والأونيرس سوري ".format(emojis["no"])
			
		if inter:
			await inter.followup.send(embed=embed(
			user=inter.user,
			desc=msg
			), 
			ephemeral=True, delete_after=10)
		else:
			await ctx.reply(embed=embed(
			user=ctx.author,
			desc=msg
			), 
			delete_after=10)
	