from nextcord import Interaction, Member
from nextcord.ext import commands; Ctx = commands.Context
from core.commands import cmds
from core import MyHelpCommand
from core.embeds import embed
from Config import emojis
import datetime

class General(commands.Cog, name="العام"):
	"""الأوامر العامة"""
	COG_EMOJI = emojis["general"]
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self
		self.cmds = cmds(self.bot)
		self.start_time = datetime.datetime.utcnow()
	
	
	#command
	@commands.command(name="leaderboard",  description="يعرض توب اعلى متصدرين", aliases=["top", "توب"], help="**الاختصارات:\n- #top\n- #توب\n**")
	async def Leaderpoard(self, ctx: commands.Context):
		await self.cmds.system.Leaderboard(ctx=ctx)
	
	#command
	@commands.command(name="uptime", aliases=["up", "وقت"])
	async def Uptime(self, ctx):
		"""يعرض اوبتايم حق البوت"""
		await self.cmds.others.Uptime(ctx=ctx, start_time=self.start_time)
	
	#command
	@commands.command(name="rep", aliases=["سمعة", "ريب"], help="**الاختصارات: (سمعة | ريب)\n- #rep @user**")
	@commands.guild_only()
	async def Rep(self, ctx, user: Member):
		"""فيي كل 24 ساعة يمكمك زيادة سمعة شخص ما"""
		await self.cmds.system.RepPoints(ctx=ctx, user=user)
	
	#command
	@commands.command(name="avatar", aliases=["صورة"], help="**- #avater @user\n-#صورة @user\n- لا تقم بتحديد اليوسر إذا كنت تريد عرض صورتك**")
	@commands.guild_only()
	async def Avatar(self, ctx, user: Member=None):
		"""عرض صورتك او صورة غيرك"""
		await self.cmds.others.Avater(ctx=ctx, user=user)
	
	#command
	@commands.command(name="transfer", aliases=["تحويل", "tr"], help="**إذا كنت لا تعرف كيف تقوم بالتحويل فلامر سهل:\n- #transfer @user 1000\n- إختصارات: (#tr | #تحويل)**")
	@commands.guild_only()
	async def Transfer(self, ctx, user: Member, coins: int):
		"""قم بتحويل عملة قضية الى عضو آخر"""
		await self.cmds.system.TransferCoins(ctx=ctx, user=user, coins=coins)
	
	#command
	@commands.command(name="daily", aliases=["تسجيل", "dy", "راتب"], help="**فقط اجمع رابتك اليومي يمكن ان تحصل على أكثر من 2500 \n- يمكنك مضاعفتها لو كنت عامل بوست - او اشتري `تنين الروح الذهبي` من المتجر**")
	@commands.guild_only()
	async def Daily(self, ctx):
		"""احصل على رابتك اليومي"""
		await self.cmds.system.Daily(ctx=ctx)
	
	#command
	@commands.command(name="profile", aliases=["pro", "بروفايل", "ملف"], help="**- مثال:\n#pro\nاو\n/profile\n- يمكنك ايضا تحديد عضو اخر لإظهار ملفه**")
	@commands.guild_only()
	async def Profile(self, ctx, user: Member = None):
		"""يقوم بعرض ملفك الشخصي او شخص آخر"""
		await self.cmds.system.Profile(ctx=ctx, user=user)
	
	#command
	@commands.command(name="ping")
	async def ping(self, ctx):
		"""يعرض البنج حق البوت"""
		latency = round(self.bot.latency * 1000)
		
		await ctx.reply(embed=embed(
			user=ctx.author,
		   desc=f"- Latency: {emojis['latency']} {latency}ms",
		   title=f"• {self.bot.user.display_name} • Latency™",
		   icon_url=self.bot.user.avatar.url
		))
	#|___________________________________________________|
	
	
	
	#------------------(بعض الفونكشنش )
	def cog_unload(self):
		self.bot.help_command = None


def setup(bot):
	bot.add_cog(General(bot))