from nextcord import Interaction, Member, Role, TextChannel
from nextcord.ext import commands; context = commands.Context
import humanfriendly
from  datetime import datetime
import time as pyTime
from core.embeds import embed, embed_done, embed_errors
from core import Helper, db
from Config import config, emojis, images
from core.ui.buttons import GiveawayButton

class OthersCommands:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#-----------------(Context commands)
	
	#function command updime
	async def Uptime(self, ctx: context, start_time):
		def convert_timedelta(duration):
			days, seconds = divmod(duration.total_seconds(), 86400)
			hours, seconds = divmod(seconds, 3600)
			minutes, seconds = divmod(seconds, 60)
			return int(days), int(hours), int(minutes), int(seconds)
		
		current_time = datetime.utcnow()
		uptime_duration = current_time - start_time
		days, hours, minutes, seconds = convert_timedelta(uptime_duration)
		await ctx.reply(embed=embed(user=ctx.author, desc=f"- أونلاين منذ\n{days} يوم، {hours} ساعة، {minutes} دقيقة، {seconds} ثانية\n-  ^_^", icon_url="https://cdn.discordapp.com/emojis/945256100935139338.png"))
		
	
	#functiion command
	async def GiveawayStart(self, ctx: context, prize, time, winners: int, channel: TextChannel=None):
		"""وظيفة الكومند إنشاء الجيفواي"""
		author = ctx.author
		if Helper.check_its_admin(author):
			if channel is None:
				channel = ctx.channel
			
			time = humanfriendly.parse_timespan(time)
			epochEnd = pyTime.time() + time
			view = GiveawayButton(time=time)
			em = embed(
				user=author,
				title=f"**🎁 • {prize} • 🎁**",
				desc=f"- {emojis['time']} الوقت: <t:{int(epochEnd)}:R>\n- 🎉 عدد الفائزين: {winners}\n{emojis['author']} تم بواسطة: {author.mention}",
				icon_url="https://cdn.discordapp.com/emojis/747504960517963957.png",
				image_url=images["bg"]
			)
			
			message = await channel.send(embed=em, view=view)
			view.message = message
			data = {
			 	"_id": message.id,
			 	"participants": [],
			 	"channel": channel.id,
			 	"time": epochEnd,
			 	"winners": winners,
			 	"hoster": author.id,
			 	"prize": prize
			 }
			db.giveaway.insert_one(data)
			await ctx.reply(embed=embed_done(desc=f"تم إنشاء  الجيفاواي في القناة {channel.mention}"), delete_after=3)
			try:
				await ctx.message.delete()
			except:
				pass
		else:
			await Helper.not_has_permisions(ctx=ctx)
	
	#function command
	async def Avater(self, ctx: context, user: Member=None):
		if user:
			desc = "استدعاء صورة {0} بواسطة {1}".format(user.mention, ctx.author.mention)
		else:
			user = ctx.author
			desc = "استدعاء صورة {0} بنجاح".format(user.mention)
		
		await ctx.reply(embed=embed(user=ctx.author,
		desc=desc, title="جلب صورة المستخدم ",
		image_url=user.display_avatar.url))
	
	#-----------------(Slash commands)-------------------
	
	#function command
	async def SetChannelNews(self, inter: Interaction, channel: TextChannel):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		guild = inter.guild
		if Helper.check_its_admin(user, owner_only=True):
			settings = Helper.guild_settings(guild)
			if settings["channel_news"] == channel.id:
				await inter.followup.send(embed=embed(user=guild.me, desc=f"تم تعيين القناة ك قناة اخبار مسبقا"))
			else:
				settings["channel_news"] = channel.id
				await inter.followup.send(embed=embed_done(desc=f"تم تعيين القناة الجريدة بنجاح شكرا"))
				
				db.settings.update_one({"_id": guild.id}, {"$set":{"channel_news": settings["channel_news"]}})
				
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
	
	#function command
	async def SetChannelLines(self, inter: Interaction, channel: TextChannel):
		await inter.response.defer(ephemeral=True)
		user = inter.user
		if Helper.check_its_admin(user, owner_only=True):
			settings = Helper.guild_settings(inter.guild)
			if channel.id in settings["auto_line_channels"]:
				settings["auto_line_channels"].remove(channel.id)
				await inter.followup.send(embed=embed_done(f"تم ازلة القناة {channel.mention} لن يتم ارسال خط  تلقائي الى هذه القناة"))
			else:
				settings["auto_line_channels"].append(channel.id)
				await inter.followup.send(embed=embed_done(desc=f"تم تعيين  القناة بنجاح {channel.mention} سيتم يتم ارسال خط  تلقائي الى هذه القناة بعد كل رسالة"))
				
			db.settings.update_one({"_id":inter.guild.id}, {"$set":{"auto_line_channels": settings["auto_line_channels"]}})
				
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
	
	#function command
	async def SetAdmin(self, inter: Interaction, role: Role):
		await inter.response.defer()
		user = inter.user
		
		if Helper.check_its_admin(user=user, owner_only=True):
			settings = Helper.guild_settings(inter.guild)
			
			if role.id in settings["admin_roles"]:
				settings["admin_roles"].remove(role.id)
				text = f"- {role.mention} لم تعد رتبة أدمن بعد الآن"
			else:
				settings["admin_roles"].append(role.id)
				text = f"- {role.mention} الآن تعتبر رتبة أدمن يمكنها استخدام كل الأوامر المسموح لرولات الأدمن إستخدامها"
			update = {
				"$set": {
					"admin_roles": settings["admin_roles"]
				}
			}
			db.settings.update_one({"_id": inter.guild.id}, update)
			await inter.followup.send(embed=embed_done(desc=text), ephemeral=True)
		
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
	
	#function command
	async def BoostMessage(self, inter:  Interaction, message):
		await inter.response.defer(ephemeral=True)
		if Helper.check_its_admin(inter.user, owner_only=True):
			
			data = Helper.guild_settings(inter.guild)
			
			data["boost_msg"] = message.id
			db.settings.update_one({"_id":inter.guild.id}, {"$set":data})
			
			await inter.followup.send(embed=embed_done(desc="تم تعيين رسالة البوست بنجاح"), ephemeral=True)
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
	
	#function command
	async def BoostChannel(self, inter:  Interaction, channel):
		await inter.response.defer(ephemeral=True)
		if Helper.check_its_admin(inter.user, owner_only=True):
			
			data = Helper.guild_settings(inter.guild)
			if data["boost_channel"] == channel.id:
				await inter.followup.send(embed=embed_errors(desc="لقد تم تعيين القماة مصبقا "), ephemeral=True)
				return
			
			data["boost_channel"] = channel.id
			db.settings.update_one({"_id":inter.guild.id}, {"$set":data})
			
			await inter.followup.send(embed=embed_done(desc="تم تعيين قناة البوست بنجاح"), ephemeral=True)
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
		
	#function command
	async def SetSuggestion(self, inter: Interaction, channel):
		await inter.response.defer(ephemeral=True)
		if Helper.check_its_admin(user=inter.user, owner_only=True):
			settings = Helper.guild_settings(inter.guild)
			if settings["suggestion_channel"] == channel.id:
				await inter.followup.send(embed=embed_errors(desc="لقد تعيين االقناة مسبقا"))
				return
			update = {
			 	"$set": {"suggestion_channel":channel.id}
			}
			db.settings.update_one({"_id":inter.guild.id}, update)
			
			await inter.followup.send(embed=embed_done(desc=f"تم تعيين قناة الإقتراحات بنجاح\n- القناة: {channel.mention}"))
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
	
	#function command
	async def SendNormalMessage(self, inter: Interaction, message, channel=None, mention="", with_line="no"):
		user = inter.user
		await inter.response.defer(ephemeral=True)
		if Helper.check_its_admin(user):
			if channel:
				await Helper.send_image_lines(channel, "line.gif", add_here_mention=True if mention != "" else False) if with_line == "yes" else None
				await channel.send(f"- {mention}\n>>> {message}")
				await Helper.send_image_lines(channel, "line.gif", add_here_mention=True if mention != "" else False) if with_line == "yes" else None
				
			else:
				await inter.channel.send(message)
			
			channel = channel if channel else inter.channel
			await inter.followup.send(embed=embed_done(desc=f"تم ارسال الرسالة الى {channel.mention} بنجاح ^_^"), ephemeral=True)
				
		else:
			await Helper.not_has_permisions(inter=inter)
	
	#functions command
	async def SendEmbed(self, inter: Interaction, title: str,desc: str, channel, image=None, with_line="yes", mention="@here"):
		"""إرسالة رسالة embed لقناة محددة"""
		user = inter.user
		await inter.response.defer(ephemeral=True)
		if Helper.check_its_admin(user):
			if with_line == "yes":
				await Helper.send_image_lines(channel, "line.gif")
			await channel.send(content=f"• {mention} •", embed=embed(
				user=user,
				title=title,
				desc=desc,
				image_url=image if image else None
			))
			if with_line=="yes":
				await Helper.send_image_lines(channel, "line.gif")
			
			await inter.followup.send(embed=embed_done(desc=f"تم ارسال الرسالة الى {channel.mention} بنجاح ^_^"), ephemeral=True)	
		else:
			await Helper.not_has_permisions(inter=inter)
	
	#function command
	async def SendDM(self, inter: Interaction, msg: str, user: Member = None, role: Role = None, is_embed="false"):
		"""كوماند ارسالة للخاص للأدمن فقط"""
		await inter.response.defer(ephemeral=True)
		if Helper.check_its_admin(inter.user, owner_only=True):
			
			if user and role:
				await inter.followup.send(embed=embed(user.inter.user, desc="اعتذر لا يمكنك تحديد اليوسر والرول في نفس الوقت"))
				return
			
			if user:
					try:
						 if is_embed == "true":
						 	await user.send(embed=embed(user=inter.user, desc=msg + f"\n\n- تم بواسطة: {inter.user.mention}"))
						 else:
						 	await user.send(f">>> **{msg}**")
						 await inter.followup.send(embed=embed_done(desc=f"تم إرسال الرسالة إلى {user.mention} بنجاح 😉"), ephemeral=True)
					except:
					 	await inter.followup.send(embed=embed_done(desc=f"فشل التنفيذ لم استطع ارسال الرسالة الى المستخدم ربما الخاص مقفل 🙂 "), ephemeral=True)
			elif role:
				cant_send = []
				for user_role in role.members:
					try:
						text = f"إلى جميع اصحاب رتبة `{role.name}` لقد تلقيتم رسالة خاصة"
						if is_embed == "true":
						 	await user_role.send(f"**@here\n- {text}**",embed=embed(user=inter.user, desc=msg))
						else:
						 	await user_role.send(f">>> **{text}\n---------\n{msg}**")
					except:
						cant_send.append(user_role.mention)
				if len(cant_send) >= 1:
						t = ", ".join(x for x in cant_send)
				else:
						t = "لا احد"
				await inter.followup.send(embed=embed(user=inter.user, desc=f"تم الارسال بنجاح الى جميع اصحاب رتبة {role.mention}\n- اشخاش لم يستلموا:\n {t}"), ephemeral=True)
			else:
				await inter.followup.send(embed=embed_errors("لم تحديد وجهت الرسالة اعتذر حد رتبة او شخص معن"))
		else:
			await Helper.not_has_permisions(inter=inter, for_owner=True)
			
		