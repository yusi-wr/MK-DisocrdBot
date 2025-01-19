import os
from urllib.parse import quote
from nextcord import Embed
from Config import config, emojis
import requests
import asyncio
import aiohttp
from core import database as db
from deep_translator import GoogleTranslator

from .icons_colors import icon, colors_types
from .collections import cards_art, cards_images, ban_stats

def Level_Scale(card):
	type = str(card["type"])
	if "xyz" in type:
		level= f"\n**Rank**: {emojis['card_rank']} {card['level']}"
	elif "Link" in type:
		level= f"\n**Link-**{card['linkval']}"
	else:
		level= f"\n**LeveL**: {emojis['card_level']} {card['level']}" if "Monster" in type else ""
		
	sclae = f" | **Scale** {card['scale']} {emojis['scale_1']}{emojis['scale_2']} {card['scale']}" if "scale" in card else ""
	return f"{level}{sclae}"


def Banlist(card):
	banlist = card["banlist_info"] if "banlist_info" in card else ""
	ban_tcg = banlist["ban_tcg"] if "ban_tcg" in banlist else "Unlimited"
	ban_ocg = banlist["ban_ocg"] if "ban_ocg" in banlist else "Unlimited"
	
	formats = card["misc_info"][0]["formats"]
	if "TCG" not in formats:
		ban_tcg = "N/A"
	if "OCG" not in formats:
		ban_ocg = "N/A"
	
	return f"- **TCG**: {ban_tcg}\n- **OCG**: {ban_ocg}"

def type_cards(card):
	
	if "Monster" in card['type']:
		mtype = str(card["type"]).replace("Monster", "").strip().replace(" ", " / ")
		TypeString = f"**Type**: {card['race']} / {mtype} / {card['attribute']}"
	elif "Trap" or "Spell" in card["type"]:
		TypeString = f"**Type**: {card['race']} {card['type'].replace('Card', '').strip()}"
	else:
		TypeString = f"**Type**: {card['type']}"
	return TypeString

class Card:
	def __init__(self, card, guild):
		self.card = card
		
		self.level = Level_Scale(card)
		self.type = type_cards(card)
		self.banlist = Banlist(card)
		self.color_card = colors_types[card["type"]] if card["type"] in colors_types else 0x414645
		self.name = card["name"]
		self.desc = card["desc"]
		self.id = str(card["id"]) if "id" in card else "0000000"
		self.url = card["ygoprodeck_url"]
		self.archetype = f"\n**Archetype**: {card['archetype']}" if "archetype" in card else ""
		self.rarity = ""
		self.card_sets = card["card_sets"] if "card_sets" in card else None
		
		if "Monster" in card["type"]:
			if "Link" in card["type"]:
				self.atk_def = f"\n**ATK**: {card['atk']}"
			else:
				self.atk_def = f"\n**ATK**: {card['atk']} / **DEF**: {card['def']}"
		else:
			self.atk_def = ""
		
		if "Monster" in card["type"]:
			self.attribute = f"{icon['icon_url'][card['attribute']] if card['attribute'] in icon['icon_url'] else ''}"
		elif "Spell" or "Trap" or "Skill" in card["type"]:
			self.attribute = f"{icon['icon_url'][card['type'].replace('Card', '').strip()] if card['type'].replace('Card', '').strip() in icon['icon_url'] else ''}"
		else:
			self.attribute = ""
		self.misc_info = card["misc_info"] if "misc_info" in card else ""
		
		try:
				self.konamiID = self.misc_info[0]["konami_id"]
		except:
				self.konamiID = "0000"
		
	async def embed_cards(self):
		
		embed = Embed(color=self.color_card)
		embed.description = f"{self.type}{self.archetype}{self.rarity}{self.level}{self.atk_def}"
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.add_field(name=f"**Effect**", value=f">>> {self.desc}")
		embed.set_thumbnail(url=cards_art[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: YUSI", icon_url="https://cdn.discordapp.com/emojis/1202030390630682725.png")
		embed.add_field(name=f"**{emojis['list']} Banlists**", value=f">>> {self.banlist}")
		
		return embed
		
	async def embed_cards_news(self):
		
		embed = Embed(color=self.color_card)
		embed.description = f"{self.type}{self.archetype}{self.rarity}{self.level}{self.atk_def}"
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.add_field(name=f"**Effect**", value=f">>> {self.desc}")
		embed.set_image(url=cards_images[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: YUSI", icon_url="https://cdn.discordapp.com/emojis/1202030390630682725.png")
		embed.add_field(name=f"**{emojis['list']} Banlists**", value=f">>> {self.banlist}")
		
		return embed
	
	async def embed_cards_ar(self):
		disc_ar = GoogleTranslator(source="auto", target="ar").translate(self.desc)
		
		embed = Embed(color=self.color_card)
		embed.description = f"{self.type}{self.archetype}{self.rarity}{self.level}{self.atk_def}"
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.add_field(name=f"**التاثير**", value=f">>> {disc_ar}")
		embed.set_thumbnail(url=cards_art[self.id]["url"])
		embed.set_footer(text=f"معرف البطاقة: {self.id} | معرفو كونامي #{self.konamiID} | تطور بواسطة: YUSI", icon_url="https://cdn.discordapp.com/emojis/1202030390630682725.png")
		embed.add_field(name=f"**{emojis['list']} البان ليست**", value=f">>> {self.banlist}")
		
		return embed
	
	async def embed_arts(self):
		
		embed = Embed(color=self.color_card)
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.set_image(url=cards_art[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: YUSI", icon_url="https://cdn.discordapp.com/emojis/1202030390630682725.png")
		
		return embed
		
	async def embed_normal_images(self):
		
		embed = Embed(color=self.color_card)
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.set_image(url=cards_images[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: YUSI", icon_url="https://cdn.discordapp.com/emojis/1202030390630682725.png")
		
		return embed
		
	async def embeds_cards_sets(self):
		embeds = []
		if self.card_sets != None:
			def func1(list_val, n):
				for x in range(0, len(list_val), n):
					yield list_val[x:x+n]
					
			def func2(lists):
				embed = Embed(color=self.color_card)
				embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
				embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: yusi_wr - YUSI", icon_url="https://cdn.discordapp.com/emojis/1202030390630682725.png")
				for x in lists:
					embed.add_field(name=f"{emojis['pointer']} **{x['set_name']}**", value=f"** - Set_Code: {x['set_code']}\n- Set_Rarity: {x['set_rarity']}\n- Rarity: {x['set_rarity_code']}\n- Set_Price: ${x['set_price']}**")
				embeds.append(embed)
			if len(self.card_sets) >= 3:
				lists = func1(self.card_sets, 3)
				for x in lists:
					func2(x)
			else:
				func2(self.card_sets)
			return embeds
		else:
			return None
				
		
		