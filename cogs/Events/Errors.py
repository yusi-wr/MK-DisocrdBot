from nextcord import Interaction
from nextcord.ext import commands
from core.embeds import embed, embed_errors
from Config import emojis

class Errors(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_application_command_error(self, interaction: Interaction, error):
		try:
			await interaction.response.defer(ephemeral=True)
		except:
			pass
		if isinstance(error, commands.errors.MemberNotFound):
			return await interaction.followup.send(embed=embed_errors(desc="اعتذر لا يتم الأثور على المستخدم في السيرفر يتم التعامل مع اعضاء الخادم فقط تأكد من ان المستخدم المطلوب موجود في نفس الخادم"), delete_after=5)
		elif isinstance(error, commands.errors.BotMissingPermissions):
			return await interaction.followup.send(embed=embed_errors("يبدو اني لا املك صلاحية لهذا يرجى تفقد رتبتي او صلحياتي\n- ايضا لا يمكنني اي تاثير على شخاص اعلى مني رتبة"), delete_after=10)
		else:
			return await interaction.followup.send(embed=embed_errors(f"الخطأ: ```{error}```"), delete_after=10)
	
	#functions event errors
	@commands.Cog.listener()
	async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""الايفنت الخاص الإيرورس"""
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.reply(embed=embed_errors(desc="اعتذر لا يتم الأثور على المستخدم في السيرفر يتم التعامل مع اعضاء الخادم فقط تأكد من ان المستخدم المطلوب موجود في نفس الخادم"), delete_after=5)
			# await ctx.message.add_reaction(emojis["no"])
			
		elif isinstance(error, commands.errors.CommandNotFound):
			await ctx.reply(embed=embed_errors(desc="الأمر المطلوب  غير موجود ×"), delete_after=5)
			#await ctx.message.add_reaction(emojis["no"])
			
		elif isinstance(error, commands.errors.BotMissingPermissions):
			await ctx.reply(embed=embed_errors("يبدو اني لا املك صلاحية لهذا يرجى تفقد رتبتي او صلحياتي\n- ايضا لا يمكنني اي تاثير على شخاص اعلى مني رتبة"))
			
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.reply(embed=embed_errors(f"هذا الأمر لديه بعض المدخلات\n- التوجيهات\n" + ctx.command.help))
		else:
			try:
				await ctx.reply(embed=embed_errors(f"الخطأ: ```{error}```"))
			except:
				return
			
def setup(bot):
	bot.add_cog(Errors(bot))