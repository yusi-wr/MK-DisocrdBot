from nextcord import Member, Role, TextChannel, utils
from nextcord.ext import commands; Ctx=commands.Context
from datetime import datetime
from core.helper import Helper
from core import db
from core.embeds import embed, embed_done, embed_errors
from random import choice
from Config import emojis


class Moderation:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#function command unmute
	async def Unmute(self, ctx: Ctx, member: Member):
		author = ctx.author
		guild = ctx.guild
		if Helper.check_its_admin(author):
			mute_role = utils.get(guild.roles, name="Muted")
			if not mute_role:
				mute_role = await guild.create_role(name="Muted")
				await ctx.reply("**جاري انشاء رتبة ميوت.......**", delete_after=3)
				for channel in guild.channels:
					try:
					    await channel.set_permissions(
			                  mute_role,
			                  speak=False,
			                   send_messages=False,
			                   read_message_history=True,
			               		 )
					except:
							continue
				if mute_role in member.roles:
					await member.remove_roles(mute_role)
					await ctx.reply(embed=embed_done(desc=f"- تم ازالة الميوت من  {member.mention} بنجاح"))
				else:
					await ctx.reply(embed=embed(user=guild.me, desc=f"اعتذر يبدو ان {member.mention} لم يتلقى اي ميوت قبلا اسف"))
		else:
			await Helper.not_has_permisions(ctx=ctx)
		
	#function command mute
	async def Mute(self, ctx: Ctx, member: Member):
		author = ctx.author
		guild = ctx.guild
		if Helper.check_its_admin(author):
			if member.id == guild.me.id:
				await ctx.reply(embed=embed(user=guild.me, desc="لا يمكنك ا تقوم بعمل ميوت لي الناس مش تقدر تستفيد من نظامي لو اتعمل لي ميوت 🙄"))
				return
			elif member.id == author.id:
				await ctx.reply(embed=embed(user=guild.me, desc="ليش تعمل لنفسك ميوت اصلا على اي حال مقدرش انفذ الامر"))
				return
			elif member.top_role.position > author.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc="مع الاسف ما تقدر تعمل ميوت لحد اعلى منك رتبة شوف حد تاني"))
				return
			elif member.top_role.position == author.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc=f"جاتك رسالة من {member.mention}\n- يااخي انا وانت نملك نفس الرتبة كيف تعمل لي ميوت 🤨"))
				return
			else:
				settings = Helper.guild_settings(guild)
				muted = settings["mute"]
				if str(member.id) in muted:
					data = muted[str(member.id)]
					muted_time = Helper.formter_other_time(data["date"], data["time_type"])
					await ctx.reply(embed=embed(user=guild.me, desc=f"ااعتذاري {author.mention} بس {member.mention} اتعمل له ميوت بالفعل\n- ينتهي بعد: {emojis['time']} {mute_time}"))
				else:
						mute_role = utils.get(guild.roles, name="Muted")
						if not mute_role:
							mute_role = await guild.create_role(name="Muted")
							await ctx.reply("**جاري انشاء رتبة ميوت.......**", delete_after=3)
							for channel in guild.channels:
								try:
								      await channel.set_permissions(
			                    mute_role,
			                    speak=False,
			                    send_messages=False,
			                    read_message_history=True,
			               					 )
								except:
									continue
						await member.add_roles(mute_role)
						await ctx.reply(embed=embed_done(desc=f"- {member.mention} اتعمل له ميوت بنجاح"))
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function command unban
	async def Unban(self, ctx: Ctx, user_id):
		author = ctx.author
		if Helper.check_its_admin(author):
			user = await self.bot.fetch_user(user_id)
			try:
				await ctx.guild.unban(user)
				await ctx.reply(embed=embed_done(f"تم تحرير {user.name} من قيود الحظر"))
			except:
				await ctx.reply(embed=embed(user=ctx.guild.me, desc=f"لم يتم الأثور على {user.name} في قائمة البان"))
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function command ban
	async def Ban(self, ctx: Ctx, member: Member, reason):
		author = ctx.author
		guild = ctx.guild
		if Helper.check_its_admin(author):
			if member.id == guild.me.id:
				await ctx.reply(embed=embed(user=guild.me, desc=choice(["ايش ذا انت عايز تبندني 😱 ", f"😅 شو رايك بي \n- #ban {author.mention} ", "روح شوف لك حد تاني انا مش حبند نفسي 😏", "شو تبي تبندني انا اوريك ابلع حشيل منك 10،000 فضة واخلى نقاط كلها 0", "جبان تبند  بوت مسكين  شوف حد قدك تلعب ضده  تحدي نقاط "])))
				return
			elif member.id == author.id:
				await ctx.reply(embed=embed(user=guild.me, desc="ليش تبند نفسك نحن نحبك نريدك معنا روح اقدي وقت ممتع مع الاخوان شوف حد تلعب معاه تحدي نقاط"))
				return
			elif member.id == guild.owner.id:
				await ctx.reply(embed=embed(user=guild.me, desc="تمام حنعمل انقلاب ونبند  الأونر وناخذ السيرفر لأنفسنا تفكير سليم 🤣\n- ده لو بدو مش يبندنا يقدر يعمل للسيرفر 🗑️ بكل شيء فيه لحيك 🤫"))
				return
			elif member.top_role.position > guild.me.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc="كيف ابند شخص اعلى مني رتبة دا لو بدوا يبندني انا وانت معا😧"))
				return
			elif member.top_role.position > author.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc=f"ما تقدر تبند {member.mention} اشان هو اعلى منك رتبة"))
				return
			elif member.top_role.position ==  author.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc=f"ما تقدر تبند {member.mention} اشان متساوين في الرتب"))
				return
			else:
				if reason is None:
					reason = f"تم بوسطة {author.name} ولم يتم تعريف السبب"
				
				await member.ban(reason=reason)
				await ctx.reply(embed=embed_done(f"{member.name} بلع بان من السيرفر 😎\n- بواسطة: {author.mention}\n- السبب: ```{reason}```\n- انا مالي دخل 😇"))
				
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	
	#function command  kick
	async def Kick(self, ctx: Ctx, member: Member, reason: str):
		author = ctx.author
		guild = ctx.guild
		if Helper.check_its_admin(author):
			if member.id == guild.me.id:
				await ctx.reply(embed=embed(user=member, desc=choice(["انت بدك تطردني بس انا عملت ايه انا اساعدكم في السيرفر كثير 😢", "شوف لك خد تاني يا عمي انا مش حقوم بطرد نفسي 😜", "بالتوفيق في المرة المقبلة 😏", "شوف الشجاع عايز يطردني انا لو بدي اطردك من الكون 😎"])))
				return
			elif member.id == author.id:
				await ctx.reply(embed=embed(user=guild.me, desc="شو المشكلة ليش تطرد نفسك ياغالي الكل بيحبك روح اقدي وقتا رائعا مع اخوتك ☺️"))
			elif member.top_role.position > author.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc="مع الأسف مش قادر انفذ طلبك اشان المعلم طلع اعلى منك رتبة 😅"))
				return
			elif member.top_role.position > guild.me.top_role.position:
				await ctx.reply(embed=embed(user=guild.me, desc="سوري بس انا مش قادر عليه شوف هو اعلى مني رتبة بينما تبي اطرده لك انا خايف انطرد 😅"))
				return
			elif member.top_role.position == author.top_role.position:
				await ctx.reply(embed=embed(user=guild.me,  desc=f"جاتك رسالة من {member.mention}\n- يبني انا وانت متساوين في  الرتبة فكيف تطرظني 🧐"))
				return
			else:
				if reason is None:
					reason = f"تم بوسطة {author.name} ولم يتم تعريف السبب"
				
				await member.kick(reason=reason)
				await ctx.reply(embed=embed_done(f"تم طرد {member.name} من الخادم \n- بواسطة: {author.mention}\n- السبب: ```{reason}```"))
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function lock channel
	async def Lock(self, ctx: Ctx, channel: TextChannel = None, role: Role = None):
		author = ctx.author
		if Helper.check_its_admin(author):
			if channel is None:
				channel = ctx.channel
			if role is None:
				role = ctx.guild.default_role
			await channel.set_permissions(role, send_messages=False)
			
			await ctx.reply(embed=embed_done(f"تم غلاق القناة بنجاح لا يمكن لي {role.mention} الكتابة في القناة"))	
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function lock channel
	async def Unlock(self, ctx: Ctx, channel: TextChannel = None, role: Role = None):
		author = ctx.author
		if Helper.check_its_admin(author):
			if channel is None:
				channel = ctx.channel
			if role is None:
				role = ctx.guild.default_role
			await channel.set_permissions(role, send_messages=True)
			
			await ctx.reply(embed=embed_done(f"تم فتح القناة بنجاح يمكن لي {role.mention} الكتابة في القناة ممن جديد"))	
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function command clear
	async def Clear(self, ctx: Ctx, amount: int, channel: TextChannel = None):
		author = ctx.author
		if Helper.check_its_admin(author):
			if channel is None:
				channel = ctx.channel
			
			if amount > 101:
				await ctx.reply(embed=embed(user=author, desc="آسف لا يمكنني حذف أكثير 100 رسالة جاري تحويل الى 100....."), delete_after=3)
				amount = 101
			amount += 1
			
			await channel.purge(limit=amount)
			await ctx.channel.send(embed=embed_done(f"تم حذف {amount} رسالة في قناة {channel.mention} بنجاح"), delete_after=10)
			
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function command add/remove role
	async def RoleCmd(self, ctx: Ctx, member: Member, role: Role, reason: str):
		author = ctx.author
		if Helper.check_its_admin(author):
			if role.position > ctx.guild.me.top_role.position:
				await ctx.reply(embed=embed_errors("يبدو أن هذه اعلى مني يجب التاكد من ان مرتبتي اعلى من هذه الرتبة"))
				return
			elif member.top_role.position > author.top_role.position:
				await ctx.reply(embed=embed(user=author, desc=f"آسف لكن {member.mention} اعلى منك رتبة لذالك لايمكنك إعطاؤه رتبة ليفعل ذالك بنفسه"))
				return
			elif member.id == author.id and role.position > author.top_role.position:
				await ctx.reply(embed=embed(user=author, desc=f"اعتذر لا يمكنك اعطاؤ نفسك رتبة اعلى منك يمكنك فقط إضافة رتبة اقل"))
				return
			elif role.position > author.top_role.position:
				await ctx.reply(embed=embed(user=author, desc=f"لايمكنك اعطاؤ احد رتبةاعلى منك "))
				return
			
			if role in member.roles:
				await member.remove_roles(role)
				if member.id == author.id:
					await ctx.reply(embed=embed_done(f"تم إزالة الرتبة بنجاح "))
				else:
					await ctx.reply(embed=embed_done(f"تم إزالة  رتبة {role.mention} من {member.mention} بنجاح\n- بواسطة: {author.mention}"))
			else:
				await member.add_roles(role)
				if member.id == author.id:
					await ctx.reply(embed=embed_done(f"تم إضافة  الرتبة اليك هههه.. اداري يضيف لنفسه رتب 🤣"))
				else:
					await ctx.reply(embed=embed_done(f"تم إضافة {role.mention} الى {member.mention} بنجاح\n- بواسطة: {author.mention}"))
		else:
			await Helper.not_has_permisions(ctx=ctx)