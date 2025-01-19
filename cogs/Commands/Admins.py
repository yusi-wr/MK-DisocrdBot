from nextcord import Interaction, Member, TextChannel, Role
import nextcord
from nextcord.ext import commands; Ctx = commands.Context
from core.commands import cmds
from Config import emojis

class Admins(commands.Cog, name="الأدمنس"):
	"""الأوامر الادارة او الادمنس"""
	COG_EMOJI = emojis["admin"]
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.cmds = cmds(self.bot)
	
		#command mute member
	@commands.command(name="unmute", help="**مثال: \n- #unmute @member**", description="الغاؤ الميوت")
	@commands.guild_only()
	async def Unute(self, ctx, member: Member):
		"""يقوم بازالة الميوت من المستخدم"""
		await self.cmds.moderation.Unmute(ctx=ctx, member=member)
			
	#command mute member
	@commands.command(name="mute", help="**مثال: \n- #mute @member**", description="اسكات امنع اي شخص من الكتابة")
	@commands.guild_only()
	async def Mute(self, ctx, member: Member):
		"""خلي شخص يبلع ميوت لوقت معين"""
		await self.cmds.moderation.Mute(ctx=ctx, member=member)
		
	#command unban members
	@commands.command(name="unban", help="**#unban ثم اكتب ID اليوسر**")
	@commands.guild_only()
	async def Unban(self, ctx, user_id: int):
		"""الغاء حظر اليوثرس"""
		await self.cmds.moderation.Unban(ctx=ctx, user_id=user_id)
	
	#command ban members
	@commands.command(name="ban", aliases=["بان", "حظر", "ابلع"], help="**الإختصارات:\n(بان | حظر | ابلع)\n- #ban @member ثم اكتب السبب**", description="حظر المستخدم من الخادم")
	@commands.guild_only()
	async def Ban(self, ctx, member:  Member, *,reason: str = None):
		"""يقوم بتبنيد عضو من السيرفر"""
		await self.cmds.moderation.Ban(ctx=ctx, member=member, reason=reason)
	
	#command kick mambers
	@commands.command(name="kick", aliases=["طرد"], help="**\n- #طرد @member\nاو\n- #kick @member ثم اكتب السبب\n- مثال:\n- #kick @user مخالفة القواعد\n- يمكنك الاستغناع عن المنشن واستخدام ID اليوسر**", description="طرد مستخدم من الخادم")
	@commands.guild_only()
	async def Kick(self, ctx, member: Member, *, reason: str  = None):
		"""يقوم بطرد يوسر من الخادم"""
		await self.cmds.moderation.Kick(ctx=ctx, member=member, reason=reason)
	
	#command lock channel
	@commands.command(name="lock", aliases=["قفل"], help="**- #فتح \n- #lock\n- #lock #channel @role\nيمكن الإستخناع عن الرتبة والقناة في حال كنت تريد تحديد القناة التي انت فيها\n- أما بخصوص تحديد الرتبة فهو لو كنت تريد منع رول معين من الكتب فيه وليس الكل**", description="اغلاق قناة")
	@commands.guild_only()
	async def Lock(self, ctx, channel: TextChannel = None, role: nextcord.Role = None):
		"""يقوم بإغلاق قناة او قناة محددة"""
		await self.cmds.moderation.Lock(ctx=ctx, channel=channel, role=role)
		
	#command lock channel
	@commands.command(name="unlock", aliases=["فتح"], help="**- #فتح \n- #unlock\n- #unlock #channel @role\nيمكن الإستخناع عن الرتبة والقناة في حال كنت تريد تحديد القناة التي انت فيها\n- أما بخصوص تحديد الرتبة فهو لو كنت منععة  الرتبة من الكتابة  سابقا باستخدام #lock**", description="فتح  القناة المغلقة")
	@commands.guild_only()
	async def Unlock(self, ctx, channel: TextChannel = None, role: nextcord.Role = None):
		"""يقوم بإغلاق قناة او قناة محددة"""
		await self.cmds.moderation.Unlock(ctx=ctx, channel=channel, role=role)
	
	#command clear msg`s
	@commands.command(name="clear", aliases=["مسح"], help="أخذف الرسائل من قناة الحالية او المحددة\n- #clear 10 #channel\n- الإفتراضي: #clear 10\n- العدد التلقائي: 10 | max: 100", description="حذف رسائل من قناة")
	@commands.guild_only()
	async def Clear(self, ctx, amount: int =10, channel: TextChannel = None):
		"""يمسح الرسائل من قناة معينة او الحالي"""
		await self.cmds.moderation.Clear(ctx=ctx, amount=amount, channel=channel)
	
	#command add/remove roles
	@commands.command(name="role", aliases=["رتبة", "رول"], help="**الاختصارات: (رول، رتبة)\n- #role @user @role\nاو\n- #role @user_id @role_id**", description="زالة/اضافة رتبة للمستخدم")
	@commands.guild_only()
	async def Role(self, ctx: Ctx, user: Member, role: Role, *, reason: str = "لم يتم تعريف اللسبب"):
		"""يقوم باضافة/ازالة رتبة من  العضو"""
		await self.cmds.moderation.RoleCmd(ctx=ctx, member=user, role=role, reason=reason)
	
	#command create giveaways
	@commands.command(name="giveaway", aliases=["gstart", "gs", "g"], help="**مثال لإستخدام: \n- #g 20k 2m 1 #channel\nالاول يشير الى الهدية المقدمة في الجيف ، الثاني يشير الى الوقت بدل  m بي s للثواني • الثالث يشير الى عدد االفائزين في الجيف كام يكون**", description="انشاء  جيف اواي")
	@commands.guild_only()
	async def Giveaway(self, ctx: commands.Context, prize, time, winners: int = 1, channel: TextChannel =None):
		"""انشاء جيف اواي"""
		await self.cmds.others.GiveawayStart(ctx=ctx, prize=prize, time=time, winners=winners, channel=channel)


def setup(bot):
	bot.add_cog(Admins(bot))