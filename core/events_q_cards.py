from .database import db
from nextcord import TextChannel
from Config import images
from random import choices, choice, randint
from .embeds import embed
from .ui import buttons

#functuon
def check_event_round(event_id):
	"""check round event"""
	check = db.events.find_one({"_id": event_id})
	return check["round"] >= check["round_count"]

#function
async def end_event(event_id: int, channel: TextChannel):
	"""formater end events {°_°}"""
	guild = channel.guild
	message = await channel.fetch_message(event_id)
	data = db.events.find_one({"_id": event_id})
	stats = data["stats"]
	prize = data["prize"]
	players = []
	for player_id in data["players"]:
		player = await guild.fetch_member(player_id)
		if player is not None:
			players.append(player.mention)
	
	role = guild.get_role(data["role_id"])
	createdBy = await guild.fetch_member(data["by"])
	winnerID = None
	text = f"- شكرا للمنظم: {createdBy.mention}\n"
	
	if len(stats) > 0:
		text += "-----------\n" + "🏆 قائمة المتصدرين 🏆\n" 
		sorted_stats = sorted(stats.items(), key=lambda x: x[1]["points"], reverse=True)
		winnerID = int(sorted_stats[0][0])
		for num, (user_id, userData) in enumerate(sorted_stats, start=1):
			text += f"{num} | {userData['user']} • {userData['points']} نقطة\n"
	else:
		text += "على ما يبدو ليس هناك اي فايزين في هذه الفعالية ياخسرة حظا موفقا للكل في المرة المقبل"
	
	em = embed(user=guild.me, desc=text, icon_url="https://cdn.discordapp.com/emojis/1106433515001761802.png", image_url=images["tournament_bg"], title="**انتهت الفعالية**")
	em.add_field(name="**تحية للأساطير 😎**", value=", ".join(x for x in players))
	await message.edit(f"• @here •", embed=em)
	await message.reply(f"{role.mention} • {createdBy.mention}", delete_after=4)
	if winnerID:
		await clim_prize(message=message, winner_id=winnerID, prize=prize)
	await role.delete()
	db.events.delete_one({"_id": event_id})

#function
async def event_start(event_id, channel: TextChannel):
	"""start event game"""
	from core.cards import cards_name, cards_art, Card, cards_data, archetypes
	
	data = db.events.find_one({"_id": event_id})
	the_round = data["round"] + 1
	end_round = data["round_count"]
	role = channel.guild.get_role(data["role_id"])
	players = data["players"]
	
	message_event = await channel.fetch_message(event_id)
	
	if len(players) == 0:
		await message_event.reply("- **الغاؤ الفعالية تلقائيا بسبب عدم مشاركة احد**")
		await role.delete()
		db.events.delete_one({"_id": event_id})
		return
	
	if data["archetype"]:
		cards_list = archetypes[data["archetype"]]
	else:
		k = randint(11, 16)
		cards_list = choices(cards_name, k=k)
	correct_name = choice(cards_list)
	card_id = Card(cards_data[correct_name], None).id
	image = cards_art[card_id]["url"]
	
	em = embed(
		user=channel.guild.me,
		desc=f"- الجولة: {end_round} / {the_round}\n- اي زر هو الإسم الصحيح لهذه البطاقة، الاعب الأسرع هو من سيفوز (^_^)",
		image_url=image
	)
	view=buttons.ViewQEvent(event_id=event_id, names=cards_list, correct=correct_name)
	msg = await message_event.reply(f"{role.mention}", embed=em, view=view)
	view.msg = msg

#function
async def clim_prize(message, winner_id, prize):
	from .helper import Helper
	from .items import Check

	guild = message.guild
	user = await guild.fetch_member(winner_id)
	
	if user is None:
		await message.reply(embed=embed(user=guild.me, desc="فشل تسليم الجايزة عدم العثور الاعب في الخادم"))
		return
	
	userData = Helper.get_user_data(user)
	send = await message.reply(embed=embed(user=user, desc=f"مبروك للفايز معنا\n- {user.mention}\n- بجايزة: ${prize:,} فضة"))
	
	check = Check(user, "207")
	if check:
		befor = prize
		prize = prize * 2
		await send.reply(embed=embed(user=user, desc="تفعيل التأثير\nتم مضاعفة الجايزة من {befor:,}$ الى {prize:,}$ بسبب تأثير `{check['name']} ^_^`", icon_url=check["icon"], title=f"**• {check['name']} •**"))
	db.users.update_one({"_id": user.id}, {"$inc": {"coins": prize}})