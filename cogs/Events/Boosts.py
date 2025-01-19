from nextcord.ext import commands
from colorama import Fore
from core import Helper, db
from core.embeds import embed_done, embed
from core.ui.buttons import ButtonSuggestion
from Config import emojis
import random

class Boosts(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.guild.premium_subscriber_role not in before.roles and after.guild.premium_subscriber_role in after.roles:
			data = Helper.guild_settings(before.guild)
			if data["boost_channel"] is None:
				return
				
			if data["boost_msg"] is None:
				text = f"الكل يحي ويقول شكراً للأسطورة {after.mention} الذي دعم السيرفر بالبوست شكراً من كل قلب ياغالي 🫡\n- بوستات الخادم الآن: {after.guild.premium_subscription_count}"
			else:
				text = data["boost_msg"] + f"\n- صار عدنا: {after.guild.premium_subscription_count} بوست"
			
			get_coins = random.randint(9500, 16000)
			db.users.update_one({"_id":after.id}, {"$inc": {"coins": get_coins}})
			text += f"لقد حصلت على {emojis['coins']} {get_coins:,}$\n- شكرا على دعم البوست"
			
			em = embed(
				user=after,
				desc=text,
				title=f"**{emojis['boost']} بوست جديد {emojis['boost']}**",
				icon_url="https://cdn.discordapp.com/emojis/906295859153608776.png"
			)
			channel = await self.bot.fetch_channel(data["boost_channel"])
			await channel.send("@here", embed=em)
		
		
def setup(bot):
	bot.add_cog(Boosts(bot))