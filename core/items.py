from .helper import Helper
from .embeds import embed, embed_done, embed_errors
from .stores import items
from .database import db
from nextcord.ext import commands
from nextcord import Interaction
from Config import emojis
from datetime import datetime
from random import choice, randint
import requests


#-----------------(Main function)--------------------
async def Use(item_id, inter: Interaction, ep=False):
	"""الفونكشن الي يحندل  تاثيرات الأيتمس المطلوبة"""
	match item_id:
		case "201":
			await Item201(inter=inter, ep=ep)
		case "202":
			await Item202(inter=inter, ep=ep)
		case "203":
			await Item203(inter=inter, ep=ep)
		case "204":
			await Item204(inter=inter, ep=ep)
		case "205":
			await Item205(inter=inter, ep=ep)
		case "206":
			await Item206(inter=inter, ep=ep)
		case "207":
			await Item207(inter=inter, ep=ep)
		case "208":
			await Item208(inter=inter, ep=ep)
		case "209":
			await Item209(inter=inter, ep=ep)
		case "210":
			await Item210(inter=inter, ep=ep)


#-------------------(فونكشنش مساعدة)----------------------
#function time text 
def text_time(date):
	return f"\n- {emojis['time']} الوقت المتبقي: {date}"

#function checker
def Check(user, items_id):
	data = Helper.get_user_data(user)["activite"]
	return items[items_id] if items_id in data else False 


#----------------(وظائف الأيتمس)---------------------
#function 201
async def Item201(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	user = inter.user
	_id = "201"
	userData = Helper.get_user_data(user)
	item = items[_id]
	
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
		
	await inter.followup.send(embed=embed(user=user, desc="في االواقعي يتم تنفيذ وظيفة التذكرة تلقائيا عند المشاركة في البطولات المدفوعة", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)

#function 202
async def Item202(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "202"
	item = items[_id]
	user = inter.user
	
	userData = Helper.get_user_data(user)
	
	if not _id in userData["items"]:
			await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
			return
	if(userData["lp"] >= 100):
			await inter.followup.send(embed=embed(user=user, desc=f"لايمكن إستخادم `{item['name']}` بينما نقاط الصحة 100% او اعلى", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
			return
	
	if Helper.check_cooldwon(user=user, cmd=_id, type=24, items=True):
	
		userData["lp"] = 100
		lp_now = userData["lp"]
		if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
		else:
			userData["items"][_id]["amount"] -= 1
		
		update = {
			"$set": {
				"lp": lp_now,
				"items": userData["items"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await inter.followup.send(embed=embed(user=user, desc=f"لقد إستخدمت {item['name']} من  الحقيبة نقاط الصحة الآن {lp_now}%", title=f"{item['name']}", icon_url=item["icon"]))
		
	else:
		text = text_time(Helper.get_cooldwon_time(user=user, cmd=_id, items=True))
		await inter.followup.send(embed=embed(user=user, desc=f"لايمكنك إستخدام `{item['name']}` الى بعد 24 ساعة" + text, title="**فشل التنفيذ**", icon_url=item["icon"]), ephemeral=ep)

#function 203
async def Item203(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	user = inter.user
	_id = "203"
	item = items[_id]
	userData = Helper.get_user_data(user)
		
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
			
	if userData["lp"] > 100:
		await inter.followup.send(embed=embed(user=user, desc=f"لايمكن إستخادم `{item['name']}` إلا إذا كانت نقاط الصحة 100% او اقل", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	userData["lp"] = 100 * 2
	lp_now = userData["lp"]
	if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
	else:
			userData["items"][_id]["amount"] -= 1
		
	update = {
		"$set": {
			"lp": lp_now,
			"items": userData["items"]
			}
		}
	db.users.update_one({"_id":user.id}, update)
	await inter.followup.send(embed=embed(user=user, desc=f"لقد إستخدمت {item['name']} من  الحقيبة نقاط الصحة الآن {lp_now}%", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)

#function 204
async def Item204(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "204"
	item = items[_id]
	user = inter.user
	
	userData = Helper.get_user_data(user)
		
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	if Helper.check_cooldwon(user=user, cmd=_id, type=24, items=True):
		
		userData["activite"][_id] = {}
		userData["activite"][_id]["date"] = str(datetime.utcnow())
		userData["activite"][_id]["type"] = 24
		if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
		else:
			userData["items"][_id]["amount"] -= 1
		update = {
			"$set": {
				"items": userData["items"],
				"activite": userData["activite"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		
		await inter.followup.send(embed=embed(user=user, desc=f"تم تفعيل تعثير {item['name']} بنجاح لن تخسر نقاط المبارزة في التحديات لمدة 24 ساعة", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
	else:
		text = text_time(Helper.get_cooldwon_time(user=user, cmd=_id, items=True))
		await inter.followup.send(embed=embed(user=user, desc=f"لايمكنك إستخدام `{item['name']}` الى بعد 24 ساعة" + text, title="**فشل التنفيذ**", icon_url=item["icon"]), ephemeral=ep)
			
#function 205
async def Item205(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "205"
	item = items[_id]
	user = inter.user
	
	userData = Helper.get_user_data(user)
	
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	if Helper.check_cooldwon(user=user, cmd=_id, type=12, items=True):
		
		userData["activite"][_id] = {}
		userData["activite"][_id]["date"] = str(datetime.utcnow())
		userData["activite"][_id]["type"] = 12
		
		if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
		else:
			userData["items"][_id]["amount"] -= 1
		update = {
			"$set": {
				"items": userData["items"],
				"activite": userData["activite"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		
		await inter.followup.send(embed=embed(user=user, desc=f"تم تفعيل تعثير {item['name']} بنجاح نقاط  السحة آمنة لمدة 12 ساعة", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
	else:
		text = text_time(Helper.get_cooldwon_time(user=user, cmd=_id, items=True))
		await inter.followup.send(embed=embed(user=user, desc=f"لايمكنك إستخدام `{item['name']}` الى بعد 12 ساعة" + text, title="**فشل التنفيذ**", icon_url=item["icon"]), ephemeral=ep)
		
		
#function 206
async def Item206(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "206"
	item = items[_id]
	user = inter.user
	userData = Helper.get_user_data(user)
	
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	choice_list = ["coins", "points", "health", "items", "coins", "coins", "points", "points", None, "coins", "coins", "health"]
	send = await inter.followup.send(embed=embed(user=user, desc="جاري .....", title=f"{item['name']}", icon_url=item["icon"]))
	for i in choice_list:
		await send.edit(embed=embed(user=user, desc=f"-----(`{i}`)--------", title=f"{item['name']}", icon_url=item["icon"]))
		
	Choice = choice(choice_list)
	
	if Choice == "coins":
		get = randint(2500, 10000)
		text = f"مباروك لقد حصلت على {emojis['coins']} {get:,}$ فضة"
		userData["coins"] += get
	elif Choice == "points":
		get = randint(10, 100)
		text = f"مبرورك لقد حصلت على {emojis['points']} {get} نقطة مبارزة ^_^"
		userData["points"] += get
	elif Choice == "health":
		get = randint(10, 50)
		text =  f"مبروك لقد حصلت على {emojis['health']['double']} {get} نقطة صحة"
		userData["lp"] += get
	elif Choice == "items":
		_idget = choice(list(items.keys()))
		itemget = items[_idget]
		name = itemget["name"]
		if len(userData["items"]) == userData["bagmax"] and _idget not in userData["items"]:
			text = f"شكلو حظك وحش 😂 أنت حصلت '`{name}`'' من المتجر بس طلع الحقيبة ممتلعة🎒 راح عليك الآيتم إشتري `رفع المستوى` اشان تطور مستوى الحقيبة 😁"
		else:
			if _idget in userData["items"]:
				userData["items"][_idget]["amount"] += 1
			else:
				userData["items"][_idget] = {}
				userData["items"][_idget]["amount"] = itemget["amount"]
			text = f"مبروك لقد حصلت على `{name}` من المتجر"
	else:
		text = f"مع الآسف حظك وحش ما حصلت حاجة 😅 جرب مرة ثاينة او روح إضرب YUSI كف 🤣"
	
	if userData["items"][_id]["amount"] == 1:
		del userData["items"][_id]
	else:
		userData["items"][_id]["amount"] -= 1
	
	if Choice != None:
		update = {
		"$set": userData
		}
	else:
		update = {
			"$set": {
				"items": userData["items"]
			}
		}
	
	db.users.update_one({"_id":user.id}, update)
	
	await send.edit(embed=embed(user=user, desc=text, title=f"{item['name']}", icon_url=item["icon"]))


#function 207
async def Item207(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "207"
	item = items[_id]
	user = inter.user
	
	userData = Helper.get_user_data(user)
	
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	if Helper.check_cooldwon(user=user, cmd=_id, type=5, items=True):
			
		userData["activite"][_id] = {}
		userData["activite"][_id]["date"] = str(datetime.utcnow())
		userData["activite"][_id]["type"] = 5
		
		if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
		else:
			userData["items"][_id]["amount"] -= 1
		update = {
			"$set": {
				"items": userData["items"],
				"activite": userData["activite"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		
		await inter.followup.send(embed=embed(user=user, desc=f"تم تفعيل تعثير {item['name']} بنجاح جميع المشتريات ونقاط التحديات و daily مضاعفة لمدة 5 ساعة", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
	else:
		text = text_time(Helper.get_cooldwon_time(user=user, cmd=_id, items=True))
		await inter.followup.send(embed=embed(user=user, desc=f"لايمكنك إستخدام `{item['name']}` الى بعد 5 ساعة" + text, title="**فشل التنفيذ**", icon_url=item["icon"]), ephemeral=ep)

#function 208
async def Item208(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "208"
	item = items[_id]
	user = inter.user
	
	userData = Helper.get_user_data(user)
		
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
		
	data = requests.get("https://db.ygoprodeck.com/api/v7/randomcard.php").json()["data"][0]
	if "Monster" in data["type"]:
			atk = data["atk"] 
			_def = data["def"]
			name = data["name"]
			get = atk + _def
			text = f"لقد حصلت على فضة تصاوي نقاط حجوم/دفاع `{name}`\n- النقاط: {emojis['coins']} {get:,}\n- الحجوم: {atk} / الدفاع: {_def}"
			
			send = await inter.followup.send(embed=embed(user=user, desc=text, title=f"{item['name']}", icon_url=item["icon"], image_url=data["card_images"][0]["image_url_cropped"]), ephemeral=ep)
			
			check = Check(user, "207")
			if check and get > 0:
				get = get * 2
				text2 = f"- تفعيل التأثير\nتم مضاعفة الفضة إلى {get}$ بنجاح بواسطة {check['name']}"
				await send.reply(embed=embed(user=user, desc=text2, title=f"**{check['name']}**", icon_url=check["icon"]))
		
			if get > 0:
				userData["coins"] += get
	else:
			type = data["type"]
			await inter.followup.send(embed=embed(user=user, desc=f"مع الآسف حظك سيء لقد حصلت على بطاقة من نوع \n-`{type}`", title=f"{item['name']}", icon_url=item["icon"], image_url=data["card_images"][0]["image_url_cropped"]), ephemeral=ep) 
		
	if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
	else:
			userData["items"][_id]["amount"] -= 1
	update = {
			"$set": {
				"coins": userData["coins"],
				"items": userData["items"]
			}
		}
	db.users.update_one({"_id":user.id}, update)

#function 209
async def Item209(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "209"
	item = items[_id]
	user = inter.user
	
	userData = Helper.get_user_data(user)
	
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	if Helper.check_cooldwon(user=user, cmd=_id, type=12, items=True):
		
		userData["activite"][_id] = {}
		userData["activite"][_id]["date"] = str(datetime.utcnow())
		userData["activite"][_id]["type"] = 12
		
		if userData["items"][_id]["amount"] == 1:
			del userData["items"][_id]
		else:
			userData["items"][_id]["amount"] -= 1
		update = {
			"$set": {
				"items": userData["items"],
				"activite": userData["activite"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		
		await inter.followup.send(embed=embed(user=user, desc=f"تم تفعيل تعثير {item['name']} بنجاح لن يتم تسجيل اي نتائج خسارة حتى في البطولات لمدة 12 ساعة", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
	else:
		text = text_time(Helper.get_cooldwon_time(user=user, cmd=_id, items=True))
		await inter.followup.send(embed=embed(user=user, desc=f"لايمكنك إستخدام `{item['name']}` الى بعد 12 ساعة" + text, title="**فشل التنفيذ**", icon_url=item["icon"]), ephemeral=ep)

#function 210
async def Item210(inter: Interaction, ep=False):
	await inter.response.defer(ephemeral=ep)
	_id = "210"
	item = items[_id]
	user = inter.user
	userData = Helper.get_user_data(user)
	
	if not _id in userData["items"]:
		await inter.followup.send(embed=embed(user=user, desc=f"فشل التنفيذ انت لا تملك هذه في حقيبتك", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)
		return
	
	maxbagBefor = userData["bagmax"]
	userData["bagmax"] += 1
	if userData["items"][_id]["amount"] == 1:
		del userData["items"][_id]
	else:
		userData["items"][_id]["amount"] -= 1
	
	update = {
		"$set": {
			"items": userData["items"],
			"bagmax": userData["bagmax"]
		}
	}
	db.users.update_one({"_id":user.id}, update)
	
	bagmax = userData["bagmax"]
	await inter.followup.send(embed=embed(user=user, desc=f"تم تطوير مستوى الحقيبة بنجاح من {maxbagBefor} الى {bagmax}", title=f"{item['name']}", icon_url=item["icon"]), ephemeral=ep)