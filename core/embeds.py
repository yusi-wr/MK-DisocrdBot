from nextcord import Embed, Color, Member
from Config import config, emojis, images
from random import choice

#functions normal embed
def embed(user:Member, desc:str, title: str=None, image_url=None, icon_url=None):
	"""تجهز embed لإستخدامه في اي وقت تمام"""
	embed = Embed(title=title, description=f"**{desc}**", color=Color.random())
	if image_url:
		embed.set_image(url=image_url)
	else:
		embed.set_image(url=images["bg"])
	if icon_url and icon_url != "":
		embed.set_thumbnail(url=icon_url)
	elif not icon_url and icon_url != "":
		embed.set_thumbnail(url=user.guild.icon.url)
	embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
	return embed
	
#function embed errors
def embed_errors(desc: str):
	"""الأمبد الي نستهدمه دائما في الايرورس"""
	embed = Embed(color=Color.red(), title=f"**{emojis['no']} اعتذر هناك خطأ ما**")
	embed.description = f">>> **{desc}**"
	embed.set_image(images["bg"])
	#embed.set_footer(text="Developed by: YUSI")
	return embed
	
#function embed done
def embed_done(desc: str):
	embed = Embed(color=Color.green(), title=f"**{emojis['yes']} تم التنفيذ بنجاح**")
	embed.description = f">>> **{desc}**"
	embed.set_image(images["bg"])
	#embed.set_footer(text="Developed by: YUSI")
	return embed

