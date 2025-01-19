from nextcord.ext import commands
import os

def Load(bot: commands.Bot):
	#قراءة الملفات الإضافية او الأوامر في ملف Cogs
	for folder in os.listdir("./cogs/"):
		for filename in os.listdir(f"./cogs/{folder}/"):
			if filename.endswith("py") and filename != "__init__.py":
					bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
					
def Unload(bot: commands.Bot):
	#إيقاف قرائة الأموامر والملفات الاضافية
	for folder in os.listdir("./cogs/"):
		for filename in os.listdir(f"./cogs/{folder}/"):
			if filename.endswith("py") and filename != "__init__.py":
					bot.unload_extension(f"cogs.{folder}.{filename[:-3]}")