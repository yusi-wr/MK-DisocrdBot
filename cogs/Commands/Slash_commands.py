from nextcord import Interaction, Member, slash_command, SlashOption, TextChannel, Attachment, Role
from nextcord.ext import commands
from core.commands import cmds
from core.helper import Helper
from core import items
from core.cards import cards_name, archetypes


QEventStartTime = {
	"بعد 24 ساعة": "24h",
	"بعد 12 ساعة": "12h",
	"بعد 5 ساعة": "5h",
	"بعد 2 ساعة": "2h",
	"بعد 1ساعة": "1h",
	"بعد 30 دقيقة": "30m",
	"بعد 10 دقايق": "10m",
	"بعد 5 دقائق": "5m",
	"بعد 10 ثواني": "10s"
}


class SlashCommands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.cmds = cmds(self.bot)
	
	#------------------(Sub cmmamds)--------------------
	@slash_command(name="send")
	async def sub_send(self, interaction):
		pass
	@slash_command(name="boost")
	async def sub_boost(self, interaction):
		pass
	@slash_command(name="store")
	async def sub_store(self, interaction):
		pass
	@slash_command(name="items")
	async def sub_items(self, interaction):
		pass
	@slash_command(name="set")
	async def sub_sets(self, interaction):
		pass
	@slash_command(name="duels")
	async def sub_duels(self, interaction):
		pass
	@slash_command(name="cards")
	async def sub_cards(self, interaction):
		pass
	#----------------------------------------#
	
	#-------------------(commands)
	
	#command
	@slash_command(name="leaderpoard", description="يعرض توب عشر متصدرين")
	async def Leaderpoard(self, interaction: Interaction):
		await self.cmds.system.Leaderboard(inter=interaction)
	
	#command
	@sub_cards.subcommand(name="events")
	async def QEventsCards(self, interaction: Interaction,
		channel: TextChannel = SlashOption(name="القناة", description="القناة التي راح نقيم فيها الفعالية"),
		start_time: str = SlashOption(name="تاريخ-البدء", description="اختر تاريخ بدء الفعالية", choices=QEventStartTime),
		prize: int = SlashOption(name="جائزة", description="اكتب رقم الفضة التي يحصل عليها الفايز في الفعالية", required=False),
		count_round: int = SlashOption(name="عدد-الجولات", description="اكتب عدد الحولات في هذه الفعالية", default=15),
		desc: str = SlashOption(name="وصف", description="هل تريد اضافة وصف خاص بك؟", default=None),
		from_archetype: str = None
		
	):
		"""انشاء فعالية اسألة بطاقات بالبوت"""
		await self.cmds.system.EventQGame(inter=interaction, start_time=start_time, count_round=count_round, channel=channel, prize=prize, desc=desc, from_archetype=from_archetype)
	
	
	#command
	@sub_cards.subcommand(name="search")
	async def SearchCards(self, interaction: Interaction,
		name: str = SlashOption(name="الإسم", description="اكتب واختر اسم البطاقة المطلوببة", required=False, default=None),
		card_id = SlashOption(name="id", description="أدخل ID البطاقة بدلا من الإسم", required=False, default=None)
		):
		"""بحث عن بطاقة بي الإسم او id"""
		await self.cmds.cards.NormalSearch(interaction=interaction, name=name, card_id=card_id)
		
	#command
	@sub_cards.subcommand(name="archetype")
	async def SearchArchetype(self, interaction: Interaction, archetype: str):
		"""بحث عن بطاقات بي archetype معين"""
		await self.cmds.cards.ArchetypeSearch(interaction=interaction, archetype=archetype)
	
	#command
	@sub_cards.subcommand(name="random")
	async def RandomSearch(self, interaction: Interaction):
		"""عرض بطاقة بشكل عشواعي"""
		await self.cmds.cards.RandomCard(interaction=interaction)
	
	@sub_cards.subcommand(name="art")
	async def ArtSearch(self, interaction: Interaction, name: str = SlashOption(name="الإسم")):
		"""إظهار كل صور art لبطاقة معينة"""
		await self.cmds.cards.ArtSearch(interaction=interaction, name=name)
		
	#command
	@sub_cards.subcommand(name="art-random")
	async def ArtRandom(self, interaction: Interaction):
		""" جلب art لبطاقة معينة بشكل عشوائي"""
		await self.cmds.cards.ArtRandom(interaction=interaction)
	
	#command
	@sub_cards.subcommand(name="image")
	async def ImageSearch(self, interaction: Interaction, name = SlashOption(name="الإسم")):
		"""جلب صور البطاقات الكاملة"""
		await self.cmds.cards.ImageSearch(interaction=interaction, name=name)
	
	#command
	@sub_cards.subcommand(name="game")
	async def Game(self, interaction: Interaction, from_archetype: str = None):
		"""لعبة التخمين البسيطة"""
		await self.cmds.cards.GameCard(interaction=interaction, archetype=from_archetype)
	
	#command
	@slash_command(name="profile")
	async def ShowProfile(self, interaction: Interaction, user: Member = SlashOption(name="المستخدم", default=None)):
		"""يقوم بعرض البرروفايل الخص بك او لغيرك"""
		await self.cmds.system.Profile(inter=interaction, user=user)
	
	#command
	@sub_duels.subcommand(name="create")
	async def CreateDuel(self, interaction: Interaction, opponent: Member = SlashOption(name="خصمك"), points: int = SlashOption(name="نقاط", description="أدخل عدد النقاط لو المباراة ابارة عن تحدي نقاط", default=None)):
		"""إنشاء مباراة عادية او تحدي نقاط بين لاعب آخير"""
		await self.cmds.system.DuelCreate(inter=interaction, opponent=opponent, points=points)
	
	#command
	@sub_duels.subcommand(name="accept")
	async def AcceptDuel(self, interaction: Interaction, winner: Member = SlashOption(name="الفائز", description="الفائز في هذه المباراة"), loser: Member = SlashOption(name="الخاسر", description="الخاسر في المباراة"), score: str = SlashOption(name="نتيجة-المباراة", description="مثال: 1-2 او 2-0 الودع التلقائي 2-1")):
		"""تأكيد مباراة بين لاعبين للأدمنس فقط"""
		await self.cmds.system.DuelAccept(inter=interaction, winner=winner, loser=loser, score=score)
	
	@sub_duels.subcommand(name="delete")
	async def DuelDeleter(self, interaction: Interaction, player1: Member = SlashOption(name="الاعب-الأول"), player2: Member = SlashOption(name="الاعب-الثاني")):
		"""يقوم بحذف مباراة معينة"""
		await self.cmds.system.DuelDeleter(inter=interaction, match_id=player1.id + player2.id)
		
	@sub_duels.subcommand(name="show")
	async def DuelShowList(self, interaction: Interaction):
		"""يقوم بعرض قائمة المباريات الحالية"""
		await self.cmds.system.DuelShowLists(inter=interaction)
	
	#command
	@sub_sets.subcommand(name="auto_line")
	async def SetLine(self, interaction: Interaction, channel: TextChannel = SlashOption(name="القناة", description="تعيين او ازالة القناة")):
		"""تعيين او ازالة خط تلقائي في القناة"""
		await self.cmds.others.SetChannelLines(inter=interaction, channel=channel)
	
	#command
	@sub_sets.subcommand(name="news")
	async def SetNews(self, interaction: Interaction, channel: TextChannel = SlashOption(name="القناة", description="تعيين او ازالة القناة")):
		"""تعيين قناة الجريدة الاخبارية"""
		await self.cmds.others.SetChannelNews(inter=interaction, channel=channel)
	
	#command
	@sub_sets.subcommand(name="coins")
	async def AddCoins(self, interaction: Interaction, user: Member = SlashOption(name="المستخدم"), coins: int = SlashOption(name="الفضة")):
		"""يقوم بإضافة نقاط فضة إلى مستخدم للأنوير فقط"""
		await self.cmds.system.AddCoins(inter=interaction, user=user, coins=coins)
	
	#command
	@sub_sets.subcommand(name="admin")
	async def SetAdmin(self, interaction: Interaction, role: Role = SlashOption(name="الرتبة", description="إزالة او إضافة أدمن رول")):
		"""تعين رتبة كأدمن او العكس للأونر فقط"""
		await self.cmds.others.SetAdmin(inter=interaction, role=role)
	
	#command
	@sub_sets.subcommand(name="nickname")
	async def SetNickname(self, interaction: Interaction, name: str = SlashOption(name="الإسم")):
		"""يمكنك من تخصيص اسم  خاص الى ملف البروفايل"""
		await self.cmds.system.SetNickname(inter=interaction, name=name)
	
	#command
	@sub_sets.subcommand(name="profile")
	async def SetProfile(self, interaction: Interaction, bg: Attachment = SlashOption(name="الصورة")):
		"""يمكنك من اضافة صورة أيقونة الى ملف البروفايل"""
		await self.cmds.system.SetProfile(inter=interaction, url=bg.url)
	
	#command
	@sub_sets.subcommand(name="background")
	async def SetBackground(self, interaction: Interaction, bg: Attachment = SlashOption(name="الصورة")):
		"""يمكنك من اضافة خلفية الى ملف البروفايل"""
		await self.cmds.system.SetBackgraound(inter=interaction, url=bg.url)
	
	#command
	@sub_items.subcommand(name="use")
	async def UseItems(self, interaction: Interaction, item_id = SlashOption(name="الإختيار", description="إختر الآيتم الذي تريد خذفه", choices=Helper.ItemsList())):
		"""إستخدام عنصر من الحقيبة"""
		await items.Use(inter=interaction, item_id=item_id)
			
	#command
	@sub_items.subcommand(name="delete")
	async def DeleteItems(self, interaction: Interaction, item_id = SlashOption(name="الإختيار", description="إختر الآيتم الذي تريد خذفه", choices=Helper.ItemsList())):
		"""يقوم بخذف آيتمس من الحقيبة"""
		await self.cmds.system.DeleteItems(inter=interaction, item_id=item_id)
	
	#command
	@sub_items.subcommand(name="show")
	async def ShowIttems(self, interaction: Interaction, user: Member = SlashOption(name="المستخدم", default=None)):
		"""يقوم باظهارر الأآستمس الخاصة بك او لغيرك"""
		await self.cmds.system.ShowItems(inter=interaction, user=user)
		
	#command
	@sub_store.subcommand(name="points")
	async def Points(self, interaction: Interaction):
		"""يقوم جميع النقاط في المتجر للشراء"""
		await self.cmds.system.StorePoints(inter=interaction)
		
	#command
	@sub_store.subcommand(name="items")
	async def Items(self, interaction: Interaction):
		"""يقوم بعرض جميع الآيتمس في اللمتجر"""
		await self.cmds.system.Store(inter=interaction)
	
	#command
	@sub_boost.subcommand(name="channel")
	async def SetBoostChannel(self, interaction: Interaction, channel: TextChannel = SlashOption(name="القناة")):
		"""تعيين قناة البوست"""
		await self.cmds.others.BoostChannel(inter=interaction, channel=channel)
	
	#command
	@sub_boost.subcommand(name="message")
	async def SetBoostMessage(self, interaction: Interaction, message = SlashOption(name="الرسالة")):
		"""تعيين رسالة البو'ست"""
		await self.cmds.others.BoostMessage(inter=interaction, message=message)
	
	#command
	@slash_command(name="suggestion")
	async def Suggestion(self, interaction: Interaction, channel: TextChannel = SlashOption(name="القناة")):
		"""يمكنك من تعيين غرفة الإقتراحات"""
		await self.cmds.others.SetSuggestion(inter=interaction, channel=channel)
		
	#command
	@sub_send.subcommand(name="message")
	async def SendMessage(self, interaction: Interaction,
		message = SlashOption(name="الرسالة"),
		channel: TextChannel = SlashOption(name="القناة", default=False),
		mention = SlashOption(name="منشن", choices={"everyone":"@everyone", "here":"@here"}, default=""),
		with_line=SlashOption(name="مع-الخط", default="no", choices={"نعم":"yes", "لا":"no"})
	):
		"""يقوم بارسالة رسالة عادية"""
		await self.cmds.others.SendNormalMessage(inter=interaction,message=message, mention=mention, with_line=with_line, channel=channel)
		
	#command
	@sub_send.subcommand(name="embed")
	async def SendEmbed(self, interaction: Interaction,
		title: str = SlashOption(name="العنوان", description="عنوان النوضوع او  title حق ال embed"),
		msg: str = SlashOption(name="الرسالة-الوصف", description="الرسالة الخاصة بال embed او  description"),
		channel: TextChannel = SlashOption(name="القناة", description="القناة التي يتم ارسال فيها الأمبيد"),
		image_url=SlashOption(name="رابط-الصورة", default=None, required=False),
		with_line=SlashOption(name="مع-الخط", default="yes", choices={"نعم":"yes", "لا":"no"}),
		mention=SlashOption(name="منشن", choices={"everyone":"@everyone", "here":"@here"}, default="@here")
	):
		"""ارسال embed الى القناة المحددة"""
		await self.cmds.others.SendEmbed(inter=interaction,title=title, desc=msg, with_line=with_line, image=image_url, channel=channel, mention=mention)
	
	#command
	@sub_send.subcommand(name="dm")
	async def SendDM(self, interaction: Interaction,
		msg: str = SlashOption(name="الرسالة", description="أكتب هنا الرسالة المطلوب"),
		user: Member = SlashOption(name="المستخدم", description="اليوسر الي راح يتم ارسالة الرسالة اليه", default=None),
		role: Role = SlashOption(name="رتبة", description="سيتم ارسال الرسالة لكل شخص معاه الرتبة", default=None),
		is_embed = SlashOption(name="خليها-embed", description="اجعل الرسالة في الأمبيد ولا لا", required=False, choices={"نعم":"true", "لا":"false"}, default="false")
	):
		"""يقوم بارسال رسالة في الخاص للأونر فقط"""
		await self.cmds.others.SendDM(inter=interaction, msg=msg, user=user, role=role, is_embed=is_embed)
	
	
	
	
	
	
	#-------------(autocomplete)
	
	#for archetype search
	@QEventsCards.on_autocomplete("from_archetype")
	@Game.on_autocomplete("from_archetype")
	@SearchArchetype.on_autocomplete("archetype")
	async def archetype_autocomplete(self, interaction, name: str):
	       if not name:
	       	await interaction.response.send_autocomplete([])
	       	return
	       
	       name = await Helper.clean(name)
	       await interaction.response.send_autocomplete([i for i in archetypes if i.startswith(name)]) if name else []
	
	#for normal search
	@ImageSearch.on_autocomplete("name")
	@ArtSearch.on_autocomplete("name")
	@SearchCards.on_autocomplete("name")
	async def searchautocomplete(self, interaction, name: str):
	       if not name:
	       	await interaction.response.send_autocomplete([])
	       	return
	       
	       name = await Helper.clean(name)
	       names = [i for i in cards_name if i.startswith(name)]
	       return await interaction.response.send_autocomplete(names) if name else []
	
	
	

def setup(bot):
	bot.add_cog(SlashCommands(bot))