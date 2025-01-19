from core import stores, items
from core.helper import Helper
from core.database import db
from core.embeds import embed_done, embed, embed_errors
from core.ui.buttons import PaginatorEmbeds, BuyItems, ViewPoints, DuelConfirm, DuelDeleteConfirm, DuelButtonDelete, ViewEventEnter
from core.ui import menus
from nextcord import Interaction, Member, TextChannel
from nextcord.ext import commands
from nextcord.ui import View
from Config import emojis, config, images
import random
import time
from datetime import datetime
from humanfriendly import parse_timespan
from random import randint

context = commands.Context

class SystemCommands:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#function command leaderboard
	async def Leaderboard(self, ctx: context = None, inter: Interaction = None):
		author = ctx.author if ctx else inter.user
		guild = ctx.guild if ctx else inter.guild
		
		em = embed(user=author, desc="هنا يتم عرض اعلى عشر متصدرين في !\n- سجل المباريات\n- نقاط المبارزة\n- عملة الفضة\nاضغط القايمة الإختيارات في الأسفل شكرا", title="**• Leaderboard DS •**")
		
		view = menus.LeaderboardViewSelect(author=author, frist_embed=em)
		if ctx:
		 	await ctx.reply(embed=em, view=view)
		else:
		 	await inter.send(embed=em, view=view)
		
	#function command event Q game cards
	async def EventQGame(self, inter: Interaction, channel: TextChannel, start_time: str, count_round: int = 15, prize: int = 10000, desc: str = None, from_archetype: str = None):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		
		if Helper.check_its_admin(user):
			the_start_ms = parse_timespan(start_time)
			start_time = time.time() + the_start_ms
			
			if desc is None:
				desc = "السلام عليكم ايها المبارزون الاساطير هل انتم مستعدين سوف ناخذكم في رحلة من التحديات والمتعة في هذه الفعالية المميزة كن الاسرع وتلغب على خصومك في الأسئلة وكن الاول الذي يخرج منتصرا"
			if prize < 2500:
				prize = randint(4000, 10000)
			
			em = embed(user=inter.guild.me, desc=desc, icon_url="https://cdn.discordapp.com/emojis/1106433515001761802.png", image_url=images["tournament_bg"], title="**YGO EVENTS**")
			em.add_field(name=f"**{emojis['cup']} الجائزة**", value=f">>> - **{emojis['coins']} {prize:,} فضة**")
			em.add_field(name=f"**{emojis['duel']} الجولات**", value=f">>> - **{count_round} جولة/جولات!**")
			em.add_field(name=f"**{emojis['time']} الوقت**", value=f">>> - **يبدء بعد: <t:{int(time.time() + the_start_ms)}:R> **")
			r = randint(993, 3550)
			role = await inter.guild.create_role(name=f"Event Q {r}")
			send = await channel.send("• @everyone •", embed=em, view=ViewEventEnter(role))
			
			data = {
				"_id": send.id,
				"players": [],
				"round_count": count_round,
				"round": 0,
				"role_id": role.id,
				"prize": prize,
				"start_time": start_time,	
				"channel": channel.id,
				"stats": {},
				"by": user.id,
				"started": "false",
				"archetype": from_archetype
				}
			
			db.events.insert_one(data)
			await inter.followup.send(embed=embed_done(f"تم انشاؤ الفعالية في {channel.mention}"))
		else:
			await Helper.not_has_permisions(inter=inter)
			
	#function commad rep
	async def RepPoints(self, ctx: context, user: Member):
		author = ctx.author
		if user.id == author.id:
			await ctx.reply(embed=embed(user=ctx.me, desc="اعتذر لا يمكنك إستخدام هذه لنفسك على شخص آخر فعلها من اجلك"), delete_after=5)
			return
		elif user.bot:
			await ctx.reply("**آسف لا يمكنك استخدام هذا علينا نحن مجرد بوتات **", delete_after=5)
			await ctx.message.delete()
			return
		if Helper.check_cooldwon(user=author, cmd="rep", type=24):
			userData = Helper.get_user_data(user)
			userData["rep"] += 1
			rep = userData["rep"]
			db.users.update_one({"_id":user.id}, {"$set":{"rep":userData["rep"]}})
			
			await ctx.send(f"{user.mention}", embed=embed(user=author, desc=f"لقد تم زيادة نقاط السمعة واصبحت {rep:,}{emojis['rep']}\n- بواسطة: {author.mention} 😉", title="**• نظام السمعة •**"))
		else:
			time = Helper.get_cooldwon_time(user=author, cmd="rep")
			await ctx.reply(embed=embed(user=ctx.me, desc=f"آسف  عليك الانتظار 24 ساعة لإعادة إستخدام هذا الكومند\nالوقت المتبقي: {emojis['time']} {time}"))
	
	#function command show user profile
	async def Profile(self, inter: Interaction = None, ctx: context = None, user= None):
		if inter:
			await inter.response.defer()
		if not user:
			user = inter.user if inter else ctx.author
		
		em = Helper.get_user_profile(user=user)
		
		if ctx:
			await ctx.reply(f"عرض ملف البروفايل {user.name}", embed=em)
		else:
			await inter.followup.send(f"عرض ملف البروفايل {user.name}", embed=em)
	
	#function command show duel list`s
	async def DuelShowLists(self, inter: Interaction):
		await inter.response.defer()
		user = inter.user
		embeds = []
		match_ids = []
		
		data_list = db.duels.find({})
		for data in data_list:
			player = await inter.client.fetch_user(data["player"])
			opponent = await inter.client.fetch_user(data["opponent"])
			match_type = data["type"]
			points = data["points"]
			date: str = data["date"]
			match_id = data["_id"]
			em = embed(user=user, desc=f"{player.mention} Vs {opponent.mention}\n- النوع: {match_type}\n- نقاط المتبادلة: {emojis['points']} {points}", title="** • Duel system™ •**", icon_url="", image_url="https://cdn.discordapp.com/attachments/1249126837091696691/1303354912276742154/2b619e42172d1c0eab902cb7b20aa419b914830429f3dcb3dfb54a8a35b66e4e._SX1080_FMpng_.png")
			em.set_footer(text=f"-  معرف المباراة: {match_id} | التاريخ: {date.split('.')[0]}")
			embeds.append(em)
			match_ids.append(match_id)
		
		if len(embeds) > 1:
			view = PaginatorEmbeds(author=user, embeds=embeds, names=match_ids)
			view.add_item(DuelButtonDelete())
			msg = await inter.followup.send(embed=embeds[0])
			view.msg = msg
		elif len(embeds) == 1:
			view = View(timeout=100)
			view.add_item(DuelButtonDelete(author=user, match_id=match_ids[0]))
			await inter.followup.send(embed=embeds[0], view=view)
		else:
			await inter.followup.send(embed=embed(user=user, desc=f"لا توجد اي مباريات في القائمة حاليا\n- االقائمة: {len(embeds)} (^_^)", title="** • Duel system™ •**"))
		
	#function command delete duels
	async def DuelDeleter(self, inter: Interaction, match_id):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		data = db.duels.find_one({"_id": match_id})
		admin_check = Helper.check_its_admin(user)
		
		if not data:
			await inter.followup.send(embed=embed(user=user, desc="لم يتم العثور على بينات لهذه المباراة", title=f"**Duel system™**"))
			return
		if not (user.id == data["player"] or user.id == data["opponent"]) and not admin_check:
			await inter.followup.send(embed=embed(user=user, desc="اعتذر ما لم تكن من الآدمنس فلا يمكنك حذف مباراة لا تخصك", title="** • Duel system™ •**"))
			return
			
		player = await inter.guild.fetch_member(data["player"])
		opponent = await inter.guild.fetch_member(data["opponent"])
		
		if not (user.id == data["player"] or user.id == data["opponent"]):
			text = f"هل انت متأكد من حذف مباراة بين {player.mention} و {opponent.mention} ?\n- ملحوظة: يتم تبليغ الاعب بعملية الحذف"
		elif user.id == opponent.id:
			text = f"هل تريد التراجع عن المباراة التي أنشاها {player.mention} ضدك ؟\n- ملحوظة: سيتم تبليغه بذالك إذا تم الخذف"
		else:
			text = f"هل حقا تريد حذف المباراة التي انشاتها ضد {opponent.mention} ?"
			
		view = DuelDeleteConfirm(author=user, _id=match_id, player=player, opponent=opponent)
		msg = await inter.followup.send(embed=embed(user=user, desc=text, title="** • Duel system™ •**", image_url="https://cdn.discordapp.com/attachments/1249126837091696691/1303354912276742154/2b619e42172d1c0eab902cb7b20aa419b914830429f3dcb3dfb54a8a35b66e4e._SX1080_FMpng_.png"), view=view)
		view.msg = msg
	
	
	#function command accept duels
	async def DuelAccept(self, inter: Interaction, winner: Member, loser: Member, score: str):
		user = inter.user
		await inter.response.defer(ephemeral=True)
		
		if Helper.check_its_admin(user):
			winnerData = Helper.get_user_data(winner)
			loserData = Helper.get_user_data(loser)
			match_id = winner.id + loser.id
			matchData = db.duels.find_one({"_id":match_id})
			
			if not matchData:
				await inter.followup.send(embed=embed(user=user, desc=f"اعتذر لم يتم العثور  على مباراة مسجلة بين {winner.mention} و {loser.mention} تأكد من انك حددت الشخص المطلوب بشكل صحيح"))
				return
			
			points = matchData["points"]
			match_type = matchData["type"]
			channel = inter.guild.get_channel(matchData["channel"])
			msg = await channel.fetch_message(matchData["msg"])
			s1 = int(score.split("-")[0])
			s2 = int(score.split("-")[1])
			if s1 > s2:
				match_score = f"{s1} - {s2}"
			else:
				match_score = f"{s2} - {s1}"
			coinsWinner = random.randint(3500, 4000)
			coinsLoser = random.randint(2500, 3000)
			
			send = await msg.reply(f" • {user.mention} | {winner.mention} Vs {loser.mention}", embed=embed(user=user, desc=f"تم تأكيد المباراة بين {winner.mention} و {loser.mention}\n- النتيجة:\n{winner.mention} {match_score} {loser.mention}\n- الفائز: {winner.mention}\n- نوع المباراة: {match_type}\n- النقاط المتبادلة: {emojis['points']} {points}\n- فضة للفائز: {emojis['coins']} {coinsWinner:,}\n- فضة للخاسر: {emojis['coins']} {coinsLoser:,}\n\n- تم بواسطة: {user.mention}", title=f"**Duel system™**", icon_url="", image_url="https://cdn.discordapp.com/attachments/1249126837091696691/1303354912276742154/2b619e42172d1c0eab902cb7b20aa419b914830429f3dcb3dfb54a8a35b66e4e._SX1080_FMpng_.png"))
			
			Item207 = items.Check(winner, "207")
			if Item207:
				coinsWinner = coinsWinner * 2 + random.randint(300, 500)
				await send.reply(embed=embed(user=loser, desc=f"تفعيل التاثير\nتم مضاعفة نقاط الفضة لي {winner.mention} الى {coinsWinner:,} نقطة  بسبب تاثير {Item207['name']}", title=f"**{Item207['name']}**", icon_url=Item207["icon"]), delete_after=35)
			
			Item207 = items.Check(loser, "207")
			if Item207:
				coinsLoser = coinsLoser * 2
				await send.reply(embed=embed(user=loser, desc=f"تفعيل التاثير\nتم مضاعفة نقاط الفضة لي {loser.mention} الى {coinsLoser:,} نقطة  بسبب تاثير {Item207['name']}", title=f"**{Item207['name']}**", icon_url=Item207["icon"]), delete_after=35)
				
			if points > 0:
				Item207 = items.Check(winner, "207")
				if Item207:
					points = points * 2
					await send.reply(embed=embed(user=loser, desc=f"تفعيل التاثير\nتم مضاعفة نقاط المباراة لي {winner.mention} الى {points} نقطة  بسبب تاثير {Item207['name']}", title=f"**{Item207['name']}**", icon_url=Item207["icon"]), delete_after=35)
				winnerData["points"] += points
				
				Item204 = items.Check(loser, "204")
				if Item204:
					await send.reply(embed=embed(user=loser, desc=f"تفعيل التاثير\nلن يخصر {loser.mention} اي نقاط بسبب تاثير {Item204['name']}", title=f"**{Item204['name']}**", icon_url=Item204["icon"]), delete_after=35)
				else:
					loserData["points"] -= points
			
			Item205 = items.Check(loser, "205")
			if Item205:
				await send.reply(embed=embed(user=loser, desc=f"تفعيل التاثير\nلن يخصر {loser.mention} اي نقاط صحة بسبب تاثير {Item205['name']}", title=f"**{Item205['name']}**", icon_url=Item205["icon"]), delete_after=35)
			else:
				Lost_lp = random.randint(7, 15)
				if loserData["lp"] < Lost_lp:
					loserData["lp"] = 0
				else:
					loserData["lp"] -= Lost_lp
			
			winnerData["duels"]["win"] += 1
			winnerData["duels"]["count"] += 1
			
			Item209 = items.Check(loser, "209")
			if Item209:
				await send.reply(embed=embed(user=loser, desc=f"تفعيل التاثير\nلن يتم تسجيل نتائج الخصارة في ملف {loser.mention}  بسبب تاثير {Item209['name']} يعني  عدد المبارياة والخسارة ستبقى كما كانت", title=f"**{Item209['name']}**", icon_url=Item209["icon"]), delete_after=35)
			else:
				loserData["duels"]["count"] += 1
				loserData["duels"]["lose"] += 1
			
			db.users.update_one({"_id":loser.id}, {"$set":loserData})
			db.users.update_one({"_id":winner.id}, {"$set":winnerData})
			db.duels.delete_one({"_id":match_id})
			
			await inter.followup.send(embed=embed_done("تم تاكيد المباراة بنجاح"))
		else:
			await Helper.not_has_permisions(inter=inter)
	
	#function command create duel vs user
	async def DuelCreate(self, inter: Interaction, opponent: Member, points: int = None):
		await inter.response.defer(ephemeral=True)
		player = inter.user
		guild = inter.guild
		
		if opponent.id == player.id:
			if points:
				await inter.followup.send(f"**يعني تلعب معك نفسك ولما تخسر تأخذ {points} {emojis['points']} من نفسك  🙄**")
			else:
				await inter.followup.send(f"**يعني ستلعب مع نفسك 🧐**")
			return
		elif opponent.bot:
			if opponent.id ==  inter.guild.me.id:
				await inter.followup.send("** ستلعب ضدي ياسلام طيب كيف احمل اللعبة 🤨**")
			else:
				await inter.followup.send(f"**ياسلام ستعلب مع {opponent.mention} وهو أصلا بوت 😒**")
			return
		
		playerData = Helper.get_user_data(player)
		opponentData = Helper.get_user_data(opponent)
		match_id = player.id + opponent.id
		
		if playerData["lp"] <= 0:
			await inter.followup.send(f"** عذرا انت متجمد نقاط صحتك 0%**")
			return
		elif opponentData["lp"] <= 0:
			await inter.followup.send("**لا يمكن طلب مباراة ضد للاعب بينما نقاط صحته 0%**")
			return
		elif points and playerData["points"] < points:
			p = playerData["points"]
			await inter.followup.send(embed=embed_errors(f"اعتذر انت لا تملك {points} نقطة \n- نقاطك: {emojis['points']} {p}"), ephemeral=True)
			return
		elif points and opponentData["points"] < points:
			p = opponentData["points"]
			await inter.followup.send(embed=embed_errors(f"اعتذر لكن {opponent.mention} لا يملك {points} نقطة \n- نقاطه: {emojis['points']} {p}"), ephemeral=True)
			return
		elif points and points > 100:
			await inter.followup.send(embed=embed(user=player, desc="أعتذر لكن يمكن التنافس بالنقاط فقط بين 100 او اقل", title="**Duel system™**"), ephemeral=True)
			return
		if points is None:
			points = 0
			mtype = "عادي"
		else:
			mtype = "تحدي نقاط"
		
		if db.duels.find_one({"_id":match_id}):
			await inter.followup.send(embed=embed(user=player, desc="عذرا هناك مباراة مسجلة بينكما بالفعل يجب خذفها تأكيدها", title="Duel system™"))
			return
			
		em = embed(user=player, desc=f"مرحبا {opponent.mention} هل تقبل المباراة ضد {player.mention}\n- النوع: {mtype}\n- النقاط: {emojis['points']} {points}\n لن تخسر اي نقاط في المباراة إذا نوع المباراة `عادي`", title="**Duel system™**", icon_url="")
		
		msg = await inter.channel.send(f"• {opponent.mention} •", embed=em)
		
		data = {
			"_id": match_id,
			"player": player.id,
			"opponent": opponent.id,
			"points": points,
			"type": mtype,
			"channel": msg.channel.id,
			"msg": msg.id,
			"date": str(datetime.utcnow()),
			"format_match": f"{player.display_name} Vs {opponent.display_name}"
		}
		view = DuelConfirm(player=player, opponent=opponent, data=data)
		view.msg = msg
		await msg.edit(view=view)
		await inter.followup.send(embed=embed_done("تم بنجاح فقط حتى يوافق خصمك على النزال"), ephemeral=True)
		
	#function command add coins into user's'
	async def AddCoins(self, inter: Interaction, user: Member, coins: int):
		await inter.response.defer(ephemeral=True)
		author = inter.user
		if Helper.check_its_admin(author, owner_only=True):
			
			if user.bot:
				await inter.followup.send("**فشل التنفيذ لازم تختار عضو مش بوت**")
				return
			
			if coins <= 0:
				await inter.followup.send(embed=embed_errors("الرقم الذي تم إدخاله غير صحيح يرجى إدخال الرقم بشكل صحيح"), ephemeral=True)
				return
			elif coins > 15000 and user.id not in self.bot.owner_ids:
				await inter.followup.send(embed=embed_errors("لا يمكن إضافة أكثر من 15,000 للمستخدم غير أونير"), ephemeral=True)
				return
			elif coins > 25000:
				await inter.followup.send(embed=embed_errors("آسف الحد الأقصى لإضافة الفضة للمستخدمين 25,000 فقط"), ephemeral=True)
				return
			
			text = f"تم إضافة {coins:,}$ إلى {user.mention}\n- بواسطة: {author.mention}"
			send = await inter.channel.send(f" • {user.mention} •", embed=embed(user=author, desc=text))
			check = items.Check(user, "207")
			if check:
				befor = coins
				coins = coins * 2
				await send.reply(embed=embed(user=user, desc=f"- تفعيل التأثير\n- تم مضاعفة الفضة من {befor:,} الى {coins:,} بسبب تأثير `{check['name']}`", title=f"**{check['name']}**", icon_url=check["icon"]))
			
			update = {
				"$inc": {
					"coins": coins
				}
			}
			db.users.update_one({"_id": user.id}, update)
		
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
		
		
	#function command set profile
	async def SetNickname(self, inter: Interaction, name: str):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		userData = Helper.get_user_data(user)
		
		price = 1700
		
		if userData["coins"] < price:
			await inter.followup.send(embed=embed(user=user, desc=f"أعتذر لا تملك مايكفي من الفضة لإنشاءإسم مخصص يجب ان تملك على الأقل {price:,}$ {emojis['points']}", title="**فشل التنفيذ !**"), ephemeral=True)
			return
		
		userData["name"] = name
		userData["coins"] -= price
		update = {
			"$set": {
				"coins": userData["coins"],
				"name": userData["name"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await inter.followup.send(embed=embed_done(desc=f"لقد تم إنشاء الاسم المخصص بنجاح\n- لقد دفعت: {emojis['coins']} {price:,}$ مقابل ذالك"))
		
	#function command set profile
	async def SetProfile(self, inter: Interaction, url: str):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		userData = Helper.get_user_data(user)
		
		price = 2100
		
		if userData["coins"] < price:
			await inter.followup.send(embed=embed(user=user, desc=f"أعتذر لا تملك مايكفي من الفضة لإضافة البروفايل يجب ان تملك على الأقل {price:,}$ {emojis['points']}", title="**فشل التنفيذ !**"), ephemeral=True)
			return
		
		userData["icon"] = url
		userData["coins"] -= price
		update = {
			"$set": {
				"coins": userData["coins"],
				"icon": userData["icon"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await inter.followup.send(embed=embed_done(desc=f"لقد تم إضافة البروفايل بنجاح\n- لقد دفعت: {emojis['coins']} {price:,}$ مقابل ذالك"))
	
	#function command set backgraound
	async def SetBackgraound(self, inter: Interaction, url: str):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		userData = Helper.get_user_data(user)
		
		price = 2500
		
		if userData["coins"] < price:
			await inter.followup.send(embed=embed(user=user, desc=f"أعتذر لا تملك مايكفي من الفضة لإضافة خلفية يجب ان تملك على الأقل {price:,}$ {emojis['coins']}", title="**فشل التنفيذ !**", image_url=url), ephemeral=True)
			return
		
		userData["bg"] = url
		userData["coins"] -= price
		update = {
			"$set": {
				"coins": userData["coins"],
				"bg": userData["bg"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await inter.followup.send(embed=embed_done(desc=f"لقد تم إضافة الخلفية بنجاح\n- لقد دفعت: {emojis['coins']} {price:,}$ مقابل ذالك"))
		
	#function command delete items
	async def DeleteItems(self, inter: Interaction, item_id):
		await inter.response.defer()
		user = inter.user
		userData = Helper.get_user_data(user)
		name = stores.items[item_id]["name"]
		icon = stores.items[item_id]["icon"]
		
		if not item_id in userData["items"]:
			view = View(timeout=None)
			view.author = user
			view.add_item(BuyItems(items_id=item_id))
			await inter.followup.send(embed=embed(user=user,desc=f"انت لا تملك {name} في الحقيبة 🎒", title=f"**{name}**", icon_url=icon), view=view)
			return
		
		del userData["items"][item_id]
		update = {
			"$set": {
				"items": userData["items"]
			}
		}
		db.users.update_one({"_id":user.id}, update)
		await inter.followup.send(embed=embed_done(desc=f"لقد تم حذف {name} من حقيبة الآيتمس خاصتك "))
	
	#function command show user items
	async def ShowItems(self, inter: Interaction, user: Member = None):
		await inter.response.defer()
		if user is None:
			user = inter.user
		userData = Helper.get_user_data(user)
		if len(userData["items"]) == 0:
			await inter.followup.send(embed=embed(user=inter.user, desc="لم يتم العثور على اي آيتمس الحقيبة فارغة"))
			return
		items = userData["items"]
		embeds = []
		items_id = []
		
		for key, values in items.items():
			item = stores.items[key]
			em = embed(user=inter.user, desc=f"- الاسم {item['name']} \n- {emojis['list']} الكمية: {values['amount']}\n- الوصف:\n{item['desc']}", title=f"** حقيبة الأغراض {user.mention}**", icon_url=item["icon"], image_url=userData["bg"])
			embeds.append(em)
			items_id.append(key)
			
		if len(embeds) > 1:
			view = PaginatorEmbeds(embeds=embeds, author=inter.user, names=items_id)
			msg = await inter.followup.send(embed=embeds[0], view=view)
			view.msg = msg
		else:
			await inter.followup.send(embed=embeds[0])
	
	#function command points store
	async def StorePoints(self, inter: Interaction):
		await inter.response.defer()
		user = inter.user
		points = stores.points
		
		text = ""
		
		for point, price in points.items():
			text += f"{emojis['points']} {point} • {emojis['coins']} ${price:,}\n"
		view = ViewPoints(store=points, author=user)
		
		msg = await inter.followup.send(embed=embed(user=user, desc=f"للشراء إضغط الرز الذي يحمل عدد النقاط الذي تريدها\n------------------\n{text}\n--------------\n- لتفعيل الايتم:\n-`/items use`", title="**متجر نقاط المبارزة**", image_url="https://images-ext-1.discordapp.net/external/XKFhiEYe12F4Fp7b-UuHsc712DfmsRVTnY5ge3d9kj8/https/i.sstatic.net/H4AdF.jpg"), view=view)
		view.msg = msg
		
	#function command store
	async def Store(self, inter: Interaction):
		await inter.response.defer()
		user = inter.user
		userData = Helper.get_user_data(user)
		items = stores.items
		embeds = []
		items_id = []
		
		for key, values in items.items():
			em = embed(user=user, title=f"**{values['name']}**", desc=f"- السعر: {emojis['coins']} {values['price']:,}\n- الكمية عند الشراء: {emojis['buy']} {values['amount']}", icon_url=values["icon"])
			em.add_field(name=f"{emojis['list']} **الوصف**", value=f">>> **{values['desc']}**")
			embeds.append(em)
			items_id.append(key)
		
		view = PaginatorEmbeds(embeds=embeds, author=user, names=items_id)
		view.add_item(BuyItems())
		msg = await inter.followup.send(embed=embeds[0], view=view)
		view.msg = msg
			
	#function command daily
	async def Daily(self, ctx: context):
		author = ctx.author
		guild = ctx.guild
		if Helper.check_cooldwon(user=author, cmd="daily", type=24):
			daily = random.randint(3500, 5000)
			if guild.premium_subscriber_role in author.roles:
				beforDaily = daily
				daily = daily * 2 + 200
				text = f"- لقد قمت بالتسجيل في راتبك اليومي بنجاح\n- حصلت على: {emojis['coins']} {beforDaily:,}$ فضة\n- تم مضاعفتها الى: {emojis['coins']} {daily:,}$ فضة\n- {emojis['boost']} يتم مضاعفة بواسطة دعم البوست {emojis['boost']}"
			else:
				text = f"- لقد قمت بالتسجيل في راتبك اليومي بنجاح\n- حصلت على: {emojis['coins']} {daily:,}$ "
			
			check = items.Check(author, "207")
			if check:
				daily = daily * 2
				text += f"\n\n- تم مضافعة نقاط daily ايضا الي ${daily:,}  بسبب تأثير `{check['name']}` مبروك"
			
			db.users.update_one({"_id":author.id}, {"$inc":{"coins":daily}})
			
			em = embed(
				user=author,
				desc=text,
				icon_url="https://cdn.discordapp.com/emojis/1221088882808848535.png",
				title="** • الراتب االيومي • **"
			)
			await ctx.reply(embed=em)
		else:
			date = Helper.get_cooldwon_time(user=author, cmd="daily")
			text = f"لقد قمت بالتسجيل في الراتب اليومي بالفعل يجب الإنتظار 24 ساعة لإعدة الإستخدامه مجددا\n- {emojis['time']} الوقت المتبقي: {date}"
			em = embed(
				user=author,
				desc=text,
				icon_url="https://cdn.discordapp.com/emojis/837883048472739840.png",
				title="** • الراتب اليومي • **"
			)
			await ctx.reply(embed=em)
	
	#function command transfer coins
	async def TransferCoins(self, ctx: context, user: Member, coins: int):
		author = ctx.author
		if user.id == ctx.guild.me.id:
			await ctx.reply("**انا مجرد بوت هعمل بها ايه😅**")
			return
		elif user.bot:
			await ctx.reply("**آسف لا يمكن التحويل للبوتات**")
			return
		authorData = Helper.get_user_data(author)
		userData = Helper.get_user_data(user)
		
		if coins <= 0:
			await ctx.reply(embed=embed_errors(desc="لا يمكن أن يكون عملية التحويل صفر او اقل "))
			return
		
		if authorData["coins"] < coins:
			await ctx.reply(embed=embed(user=author, desc=f"أذن انك لا تملك ما يكفي للتحويل\n- تملك: {emojis['coins']} {authorData['coins']:,} فضة", title="**فشل التحويل**"))
			return
		
		userData["coins"] += coins
		authorData["coins"] -= coins
		update_user = {
			"$set": {
				"coins": userData["coins"]
			}
		}
		update_author = {"$set": {
				"coins": authorData["coins"]
			}
		}
		db.users.update_one({"_id": user.id}, update_user)
		db.users.update_one({"_id": author.id}, update_author)
		
		try:
			await user.send(embed=embed(user=author, desc=f"لقد تلقيت تحويلا: {emojis['coins']} {coins:,} فضة\n- بواسطة {author.mention}", title="**إيصال التحويل**"))
		except:
			pass
		
		await ctx.reply(embed=embed_done(f"تم تحويل: {emojis['coins']} {coins:,} فضة الى {user.mention} بنجاح\n- بواسطة {author.mention}"))