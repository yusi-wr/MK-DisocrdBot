import nextcord
from nextcord.ext import commands, tasks
from Config import config
import os
from core import extensions
from core.embeds import embed
from dotenv import load_dotenv, find_dotenv
import asyncio
from keep_alive import keep_alive


load_dotenv(find_dotenv())

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents, case_insensitive=True, strip_after_prefix=True, owner_ids=config["owners"])

#لا تحذف ولا تغيير الا لو كنت تعرف انت تعمل ايه
@bot.slash_command(name="extensions")
async def sub_extensions(interaction):
	pass

#لا تحذف ولا تغيير الا لو كنت تعرف انت تعمل ايه
@sub_extensions.subcommand(name="unload", description="يقوم بإقاف البوت عن العمل والأوامر")
async def UnloadExtensions(interaction: nextcord.Interaction):
	from core import Helper
	await interaction.response.defer(ephemeral=True)
	if Helper.check_its_admin(interaction.user, owner_only=True):
		extensions.Unload(bot)
		await interaction.followup.send("إيقاف عمل الأوامر والاحداث بناج", ephemeral=True)
	else:
		await Helper.not_has_permisions(inter=interaction, for_owner=True)

#لا تحذف ولا تغيير الا لو كنت تعرف انت تعمل ايه
@sub_extensions.subcommand(name="load", description="لأعادة تنشيط الأوامر والأحداث")
async def LoadExtensions(interaction: nextcord.Interaction):
	from core import Helper
	await interaction.response.defer(ephemeral=True)
	if Helper.check_its_admin(interaction.user, owner_only=True):
		extensions.Load(bot)
		await interaction.followup.send("إعادة تنشيط  الاوامر بنجاح", ephemeral=True)
	else:
		await Helper.not_has_permisions(inter=interaction, for_owner=True)



if __name__ == "__main__":
	extensions.Load(bot)
	keep_alive()
	bot.run(os.getenv("TOKEN"))